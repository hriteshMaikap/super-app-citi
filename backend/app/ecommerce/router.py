"""
E-commerce routes for product search and management
FAISS-powered semantic search with MongoDB backend
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional, List
import logging
import uuid

from ..core.database import get_db
from ..schemas.ecommerce import (
    ProductSearchRequest, ProductSearchResponse, ProductDetailRequest,
    ProductDetailResponse, WishlistRequest, WishlistResponse,
    SearchAnalyticsResponse, SearchSuggestionResponse
)
from ..ecommerce.service import ecommerce_service
from ..auth.dependencies import get_current_user, get_client_info
from ..models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ecommerce", tags=["ecommerce"])


@router.post("/search", response_model=ProductSearchResponse)
async def search_products(
    search_request: ProductSearchRequest,
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ProductSearchResponse:
    """
    Search products using semantic similarity with FAISS
    
    - **query**: Search query (e.g., "smartphone with good camera")
    - **limit**: Number of results (1-50, default 5)
    - **category_filter**: Filter by category (optional)
    - **price_min/price_max**: Price range filters (optional)
    - **brand_filter**: Filter by brand (optional)
    - **in_stock_only**: Show only in-stock products (default true)
    - **min_rating**: Minimum rating filter (optional)
    
    **Features:**
    - Semantic search using sentence transformers
    - FAISS vector similarity for fast retrieval
    - Advanced filtering capabilities
    - Search analytics and suggestions
    """
    try:
        # Get client info
        client_info = get_client_info(request)
        user_id = current_user.user_id if current_user else None
        session_id = request.headers.get("x-session-id", str(uuid.uuid4()))
        
        # Perform search
        result = await ecommerce_service.search_products(
            search_request=search_request,
            user_id=user_id,
            session_id=session_id,
            db=db
        )
        
        logger.info(f"Product search completed: query='{search_request.query}', results={result.total_results}")
        
        return result
        
    except Exception as e:
        logger.error(f"Product search failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Product search failed"
        )


@router.get("/product/{product_id}", response_model=ProductDetailResponse)
async def get_product_detail(
    product_id: str,
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ProductDetailResponse:
    """
    Get detailed product information
    
    - **product_id**: MongoDB product ID
    
    **Returns:**
    - Complete product details
    - Similar products
    - Product analytics (views, sales)
    - Specifications and metadata
    """
    try:
        # Get client info
        client_info = get_client_info(request)
        user_id = current_user.user_id if current_user else None
        session_id = request.headers.get("x-session-id", str(uuid.uuid4()))
        
        # Get product detail
        result = await ecommerce_service.get_product_detail(
            product_id=product_id,
            user_id=user_id,
            session_id=session_id,
            db=db
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get product detail failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get product details"
        )


@router.post("/wishlist/add")
async def add_to_wishlist(
    wishlist_request: WishlistRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Add product to user's wishlist
    
    - **product_id**: MongoDB product ID
    - **notes**: Optional personal notes about the product
    """
    try:
        success = await ecommerce_service.add_to_wishlist(
            user_id=current_user.user_id,
            product_id=wishlist_request.product_id,
            notes=wishlist_request.notes,
            db=db
        )
        
        if success:
            return {"message": "Product added to wishlist successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product not found or already in wishlist"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Add to wishlist failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add product to wishlist"
        )


@router.get("/wishlist", response_model=List[ProductDetailResponse])
async def get_wishlist(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> List[ProductDetailResponse]:
    """
    Get user's wishlist products
    
    **Returns:**
    - List of products in user's wishlist
    - Complete product details for each item
    """
    try:
        products = await ecommerce_service.get_user_wishlist(
            user_id=current_user.user_id,
            db=db
        )
        
        return products
        
    except Exception as e:
        logger.error(f"Get wishlist failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get wishlist"
        )


@router.get("/suggestions", response_model=SearchSuggestionResponse)
async def get_search_suggestions(
    q: str = Query(..., min_length=1, max_length=100, description="Query prefix for suggestions")
) -> SearchSuggestionResponse:
    """
    Get search suggestions based on query prefix
    
    - **q**: Query prefix (e.g., "smart" -> "smartphone", "smartwatch")
    
    **Returns:**
    - Autocomplete suggestions
    - Trending searches
    - Popular categories and brands
    """
    try:
        # Simple suggestion logic (in production, use more sophisticated approaches)
        suggestions = []
        
        # Basic keyword matching
        keywords = {
            "smart": ["smartphone", "smartwatch", "smart TV", "smart home"],
            "phone": ["smartphone", "phone case", "phone charger"],
            "laptop": ["laptop", "laptop bag", "laptop stand"],
            "head": ["headphones", "headset", "head massager"],
            "shoe": ["shoes", "shoe rack", "shoe cleaner"],
            "coffee": ["coffee maker", "coffee beans", "coffee mug"],
            "book": ["books", "bookshelf", "bookmark"],
            "watch": ["watch", "smartwatch", "watch band"]
        }
        
        for keyword, matches in keywords.items():
            if keyword in q.lower():
                suggestions.extend([match for match in matches if q.lower() in match.lower()])
        
        # Remove duplicates and limit
        suggestions = list(set(suggestions))[:5]
        
        response = SearchSuggestionResponse(
            suggestions=suggestions,
            trending=["smartphone", "laptop", "headphones", "sneakers"],
            categories=["Electronics", "Fashion", "Home & Kitchen", "Sports"],
            brands=["Apple", "Samsung", "Nike", "Sony", "Adidas"]
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Get suggestions failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get suggestions"
        )


@router.post("/admin/refresh-index")
async def refresh_search_index(
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Admin endpoint to refresh FAISS search index
    
    **Note:** This endpoint should be restricted to admin users in production
    """
    try:
        # In production, add admin role check here
        # if not current_user.is_admin:
        #     raise HTTPException(status_code=403, detail="Admin access required")
        
        ecommerce_service.refresh_search_index()
        
        return {"message": "Search index refreshed successfully"}
        
    except Exception as e:
        logger.error(f"Refresh index failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh search index"
        )


@router.get("/categories")
async def get_categories() -> Dict[str, List[str]]:
    """
    Get available product categories and subcategories
    
    **Returns:**
    - List of main categories
    - Subcategories for each main category
    """
    try:
        # Static categories (in production, fetch from MongoDB)
        categories = {
            "Electronics": [
                "Smartphones", "Laptops", "Tablets", "Audio", "Cameras", 
                "Television", "Gaming", "Accessories"
            ],
            "Fashion": [
                "Clothing", "Footwear", "Accessories", "Outerwear", "Activewear"
            ],
            "Home & Kitchen": [
                "Appliances", "Cookware", "Small Appliances", "Cleaning", "Drinkware"
            ],
            "Sports": [
                "Running", "Fitness", "Accessories", "Wearables", "Recovery"
            ],
            "Beauty": [
                "Hair Care", "Makeup", "Skincare", "Tools"
            ],
            "Books": [
                "E-readers", "Fiction", "Non-fiction", "Educational"
            ],
            "Automotive": [
                "Electric Vehicles", "Accessories", "Parts"
            ],
            "Toys": [
                "Building Sets", "Educational", "Games"
            ],
            "Furniture": [
                "Office", "Living Room", "Bedroom"
            ],
            "Home & Garden": [
                "Grills", "Outdoor", "Tools"
            ]
        }
        
        return categories
        
    except Exception as e:
        logger.error(f"Get categories failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get categories"
        )


@router.get("/brands")
async def get_brands() -> List[str]:
    """
    Get popular brands
    
    **Returns:**
    - List of popular brands
    """
    try:
        # Static brands (in production, fetch from MongoDB)
        brands = [
            "Apple", "Samsung", "Nike", "Adidas", "Sony", "LG", "Canon", 
            "Dell", "HP", "Bose", "Ray-Ban", "Patagonia", "Allbirds",
            "KitchenAid", "Levi's", "Dyson", "Instant Pot", "Nespresso",
            "Le Creuset", "Peloton", "Hydro Flask", "Garmin", "Glossier",
            "Amazon", "Tesla", "LEGO", "Vitamix", "Herman Miller", "Weber",
            "Ninja", "Fitbit", "Breville", "Yeti", "Sonos", "Stanley",
            "Therabody", "Ember"
        ]
        
        return sorted(brands)
        
    except Exception as e:
        logger.error(f"Get brands failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get brands"
        )


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for e-commerce service"""
    
    try:
        # Check FAISS availability
        faiss_status = "available" if ecommerce_service.vector_engine.faiss_index is not None else "unavailable"
        embeddings_status = "available" if ecommerce_service.vector_engine.embeddings_model is not None else "unavailable"
        
        return {
            "status": "healthy",
            "service": "ecommerce",
            "faiss_index": faiss_status,
            "embeddings_model": embeddings_status,
            "features": {
                "semantic_search": faiss_status == "available",
                "product_details": "available",
                "wishlist": "available",
                "analytics": "available"
            }
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "ecommerce",
            "error": str(e)
        }