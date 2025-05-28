"""
E-commerce service with FAISS vector search
Product search using sentence transformers and semantic similarity
"""
import asyncio
import json
import time
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging
import os

from pymongo import MongoClient
from bson import ObjectId
import numpy as np

# Import FAISS and HuggingFace components
try:
    import faiss
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logging.warning("FAISS or sentence-transformers not available. Install with: pip install faiss-cpu sentence-transformers")

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from ..core.config import settings
from ..models.ecommerce import SearchQuery, ProductView, UserWishlist
from ..schemas.ecommerce import (
    ProductSearchRequest, ProductSearchResponse, ProductResponse,
    ProductDetailResponse, SearchAnalyticsResponse
)

logger = logging.getLogger(__name__)


class VectorSearchEngine:
    """FAISS-based vector search engine for products"""
    
    def __init__(self):
        self.embeddings_model = None
        self.faiss_index = None
        self.product_ids = []
        self.products_data = []
        self.index_path = "backend/data/faiss_index"
        self.products_path = "backend/data/products_data.json"
        
        if FAISS_AVAILABLE:
            self._initialize_model()
            self._load_or_create_index()
    
    def _initialize_model(self):
        """Initialize the sentence transformer model"""
        try:
            self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")
            self.embeddings_model = None
    
    def _load_or_create_index(self):
        """Load existing FAISS index or create new one"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs("backend/data", exist_ok=True)
            
            # Try to load existing index
            if os.path.exists(f"{self.index_path}.faiss") and os.path.exists(self.products_path):
                self._load_index()
                logger.info("Loaded existing FAISS index")
            else:
                # Create new index from MongoDB
                self._create_index_from_mongodb()
                logger.info("Created new FAISS index from MongoDB")
                
        except Exception as e:
            logger.error(f"Failed to load/create FAISS index: {e}")
            self.faiss_index = None
    
    def _load_index(self):
        """Load FAISS index and product data"""
        try:
            # Load FAISS index
            self.faiss_index = faiss.read_index(f"{self.index_path}.faiss")
            
            # Load product data
            with open(self.products_path, 'r') as f:
                data = json.load(f)
                self.products_data = data['products']
                self.product_ids = data['product_ids']
                
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            raise
    
    def _save_index(self):
        """Save FAISS index and product data"""
        try:
            # Save FAISS index
            faiss.write_index(self.faiss_index, f"{self.index_path}.faiss")
            
            # Save product data
            data = {
                'products': self.products_data,
                'product_ids': self.product_ids,
                'created_at': datetime.utcnow().isoformat(),
                'total_products': len(self.products_data)
            }
            
            with open(self.products_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
            logger.info(f"Saved FAISS index with {len(self.products_data)} products")
            
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise
    
    def _create_index_from_mongodb(self):
        """Create FAISS index from MongoDB products"""
        if not self.embeddings_model:
            logger.error("Embeddings model not available")
            return
        
        try:
            # Connect to MongoDB
            client = MongoClient(settings.mongodb_uri)
            db = client[settings.mongodb_db_name]
            collection = db["products"]
            
            # Fetch all products
            products = list(collection.find())
            
            if not products:
                logger.warning("No products found in MongoDB")
                return
            
            logger.info(f"Processing {len(products)} products from MongoDB")
            
            # Prepare text for embedding
            texts = []
            self.products_data = []
            self.product_ids = []
            
            for product in products:
                # Create searchable text combining name, description, and tags
                searchable_text = f"{product['name']} {product['description']} {' '.join(product.get('tags', []))}"
                texts.append(searchable_text)
                
                # Store product data (convert ObjectId to string)
                product_data = {k: str(v) if isinstance(v, ObjectId) else v for k, v in product.items()}
                self.products_data.append(product_data)
                self.product_ids.append(str(product['_id']))
            
            # Generate embeddings
            logger.info("Generating embeddings...")
            embeddings = self.embeddings_model.encode(texts, show_progress_bar=True)
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            self.faiss_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add embeddings to index
            self.faiss_index.add(embeddings.astype('float32'))
            
            # Save index
            self._save_index()
            
            logger.info(f"Successfully created FAISS index with {len(products)} products")
            
        except Exception as e:
            logger.error(f"Failed to create index from MongoDB: {e}")
            raise
        finally:
            if 'client' in locals():
                client.close()
    
    def search(self, query: str, k: int = 2, filters: Dict[str, Any] = None) -> List[Tuple[Dict[str, Any], float]]:
        """Search products using semantic similarity"""
        if not self.faiss_index or not self.embeddings_model:
            logger.error("Search engine not properly initialized")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embeddings_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search in FAISS index
            scores, indices = self.faiss_index.search(query_embedding.astype('float32'), k * 2)  # Get more results for filtering
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx != -1:  # Valid index
                    product = self.products_data[idx].copy()
                    
                    # Apply filters if provided
                    if self._passes_filters(product, filters):
                        results.append((product, float(score)))
                    
                    # Stop when we have enough results
                    if len(results) >= k:
                        break
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def _passes_filters(self, product: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if product passes the applied filters"""
        if not filters:
            return True
        
        try:
            # Category filter
            if filters.get('category_filter') and product.get('category', '').lower() != filters['category_filter'].lower():
                return False
            
            # Brand filter
            if filters.get('brand_filter') and product.get('brand', '').lower() != filters['brand_filter'].lower():
                return False
            
            # Price filters
            product_price = float(product.get('price', 0))
            if filters.get('price_min') and product_price < filters['price_min']:
                return False
            if filters.get('price_max') and product_price > filters['price_max']:
                return False
            
            # Stock filter
            if filters.get('in_stock_only', True) and not product.get('in_stock', False):
                return False
            
            # Rating filter
            if filters.get('min_rating') and float(product.get('rating', 0)) < filters['min_rating']:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Filter check failed: {e}")
            return True  # If filter check fails, include the product
    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get product by MongoDB ID with fallback to local data"""
        try:
            # First try to connect to MongoDB for real-time data
            client = MongoClient(settings.mongodb_uri)
            db = client[settings.mongodb_db_name]
            collection = db["products"]
            
            product = collection.find_one({"_id": ObjectId(product_id)})
            
            if product:
                # Convert ObjectId to string
                product['_id'] = str(product['_id'])
                return product
                
        except Exception as e:
            logger.error(f"Failed to get product from MongoDB: {e}, falling back to local data")
        finally:
            if 'client' in locals():
                client.close()
        
        # Fallback to local JSON data if MongoDB is unavailable
        try:
            if os.path.exists(self.products_path):
                with open(self.products_path, 'r') as f:
                    data = json.load(f)
                    products = data.get('products', [])
                    
                    # Search for product by ID
                    for product in products:
                        if str(product.get('_id')) == product_id:
                            return product
                            
            logger.warning(f"Product {product_id} not found in local data")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get product from local data: {e}")
            return None
    
    def refresh_index(self):
        """Refresh the FAISS index with latest MongoDB data"""
        logger.info("Refreshing FAISS index...")
        self._create_index_from_mongodb()


class EcommerceService:
    """E-commerce service for product search and management"""
    
    def __init__(self):
        self.vector_engine = VectorSearchEngine()
    
    async def search_products(
        self,
        search_request: ProductSearchRequest,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        db: Optional[AsyncSession] = None
    ) -> ProductSearchResponse:
        """Search products using semantic similarity"""
        
        start_time = time.time()
        search_id = str(uuid.uuid4())
        
        try:
            # Prepare filters
            filters = {}
            if search_request.category_filter:
                filters['category_filter'] = search_request.category_filter
            if search_request.brand_filter:
                filters['brand_filter'] = search_request.brand_filter
            if search_request.price_min is not None:
                filters['price_min'] = search_request.price_min
            if search_request.price_max is not None:
                filters['price_max'] = search_request.price_max
            if search_request.min_rating is not None:
                filters['min_rating'] = search_request.min_rating
            filters['in_stock_only'] = search_request.in_stock_only
            
            # Perform vector search
            search_results = self.vector_engine.search(
                search_request.query,
                k=search_request.limit,
                filters=filters
            )
            
            # Convert results to response format
            products = []
            for product_data, relevance_score in search_results:
                product_response = ProductResponse(
                    product_id=str(product_data['_id']),
                    name=product_data['name'],
                    description=product_data['description'],
                    category=product_data['category'],
                    subcategory=product_data['subcategory'],
                    price=float(product_data['price']),
                    currency=product_data['currency'],
                    seller=product_data['seller'],
                    brand=product_data['brand'],
                    rating=float(product_data['rating']),
                    reviews_count=int(product_data['reviews_count']),
                    in_stock=bool(product_data['in_stock']),
                    stock_quantity=int(product_data['stock_quantity']),
                    tags=product_data['tags'],
                    specifications=product_data['specifications'],
                    relevance_score=relevance_score,
                    free_shipping=product_data.get('free_shipping', False)
                )
                products.append(product_response)
            
            # Calculate search time
            search_time_ms = (time.time() - start_time) * 1000
            
            # Log search query
            if db:
                await self._log_search_query(
                    search_request.query,
                    len(products),
                    search_time_ms,
                    user_id,
                    session_id,
                    db
                )
            
            # Get suggested filters and related searches
            suggested_filters = await self._get_suggested_filters(search_results)
            related_searches = await self._get_related_searches(search_request.query)
            
            response = ProductSearchResponse(
                query=search_request.query,
                total_results=len(products),
                search_time_ms=search_time_ms,
                products=products,
                search_id=search_id,
                applied_filters=filters,
                suggested_filters=suggested_filters,
                related_searches=related_searches,
                trending_searches=await self._get_trending_searches()
            )
            
            return response

        except Exception as e:
            logger.error(f"Product search failed: {e}")
            # Return empty results on error
            return ProductSearchResponse(
                query=search_request.query,
                total_results=0,
                search_time_ms=(time.time() - start_time) * 1000,
                products=[],
                search_id=search_id,
                applied_filters={},
                suggested_filters={},
                related_searches=[],
                trending_searches=[]
            )

    async def get_product_detail(
        self,
        product_id: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        db: Optional[AsyncSession] = None
    ) -> Optional[ProductDetailResponse]:
        """Get detailed product information"""
        
        try:
            # Get product from MongoDB
            product_data = self.vector_engine.get_product_by_id(product_id)
            
            if not product_data:
                return None
            
            # Log product view
            if db:
                await self._log_product_view(product_id, user_id, session_id, db)
            
            # Get similar products
            similar_products = await self._get_similar_products(product_data, limit=2)
            
            # Create detailed response
            product_detail = ProductDetailResponse(
                product_id=str(product_data['_id']),
                name=product_data['name'],
                description=product_data['description'],
                category=product_data['category'],
                subcategory=product_data['subcategory'],
                price=float(product_data['price']),
                currency=product_data['currency'],
                seller=product_data['seller'],
                brand=product_data['brand'],
                rating=float(product_data['rating']),
                reviews_count=int(product_data['reviews_count']),
                in_stock=bool(product_data['in_stock']),
                stock_quantity=int(product_data['stock_quantity']),
                tags=product_data['tags'],
                specifications=product_data['specifications'],
                views=int(product_data.get('views', 0)),
                sales_count=int(product_data.get('sales_count', 0)),
                featured=bool(product_data.get('featured', False)),
                warranty_months=int(product_data.get('warranty_months', 12)),
                returnable=bool(product_data.get('returnable', True)),
                created_at=product_data.get('created_at', datetime.utcnow()),
                updated_at=product_data.get('updated_at', datetime.utcnow()),
                free_shipping=product_data.get('free_shipping', False),
                similar_products=similar_products
            )
            
            return product_detail
            
        except Exception as e:
            logger.error(f"Get product detail failed: {e}")
            return None
    
    async def add_to_wishlist(
        self,
        user_id: str,
        product_id: str,
        notes: Optional[str] = None,
        db: AsyncSession = None
    ) -> bool:
        """Add product to user's wishlist"""
        
        try:
            # Check if product exists
            product = self.vector_engine.get_product_by_id(product_id)
            if not product:
                return False
            
            # Check if already in wishlist
            existing = await db.execute(
                select(UserWishlist).where(
                    and_(
                        UserWishlist.user_id == user_id,
                        UserWishlist.product_id == product_id
                    )
                )
            )
            
            if existing.scalars().first():
                return False  # Already in wishlist
            
            # Add to wishlist
            wishlist_item = UserWishlist(
                user_id=user_id,
                product_id=product_id,
                notes=notes,
                added_from="manual"
            )
            
            db.add(wishlist_item)
            await db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Add to wishlist failed: {e}")
            return False
    
    async def get_user_wishlist(
        self,
        user_id: str,
        db: AsyncSession
    ) -> List[ProductResponse]:
        """Get user's wishlist products"""
        
        try:
            # Get wishlist items
            result = await db.execute(
                select(UserWishlist).where(UserWishlist.user_id == user_id)
            )
            wishlist_items = result.scalars().all()
            
            products = []
            for item in wishlist_items:
                product_data = self.vector_engine.get_product_by_id(item.product_id)
                if product_data:
                    product_response = ProductResponse(
                        product_id=str(product_data['_id']),
                        name=product_data['name'],
                        description=product_data['description'],
                        category=product_data['category'],
                        subcategory=product_data['subcategory'],
                        price=float(product_data['price']),
                        currency=product_data['currency'],
                        seller=product_data['seller'],
                        brand=product_data['brand'],
                        rating=float(product_data['rating']),
                        reviews_count=int(product_data['reviews_count']),
                        in_stock=bool(product_data['in_stock']),
                        stock_quantity=int(product_data['stock_quantity']),
                        tags=product_data['tags'],
                        specifications=product_data['specifications'],
                        free_shipping=product_data.get('free_shipping', False)
                    )
                    products.append(product_response)
            
            return products
            
        except Exception as e:
            logger.error(f"Get wishlist failed: {e}")
            return []
    
    # Helper methods
    async def _log_search_query(
        self,
        query: str,
        results_count: int,
        response_time_ms: float,
        user_id: Optional[str],
        session_id: Optional[str],
        db: AsyncSession
    ):
        """Log search query for analytics"""
        
        try:
            search_log = SearchQuery(
                user_id=user_id,
                query_text=query,
                results_count=results_count,
                response_time_ms=response_time_ms,
                session_id=session_id,
                search_type="semantic"
            )
            
            db.add(search_log)
            await db.commit()
            
        except Exception as e:
            logger.error(f"Failed to log search query: {e}")
    
    async def _log_product_view(
        self,
        product_id: str,
        user_id: Optional[str],
        session_id: Optional[str],
        db: AsyncSession
    ):
        """Log product view for analytics"""
        
        try:
            view_log = ProductView(
                user_id=user_id,
                product_id=product_id,
                session_id=session_id,
                device_type="web"
            )
            
            db.add(view_log)
            await db.commit()
            
        except Exception as e:
            logger.error(f"Failed to log product view: {e}")
    
    async def _get_similar_products(
        self,
        product_data: Dict[str, Any],
        limit: int = 2
    ) -> List[ProductResponse]:
        """Get similar products based on category and tags"""
        
        try:
            # Create search query from product category and tags
            search_query = f"{product_data['category']} {product_data['subcategory']} {' '.join(product_data.get('tags', []))}"
            
            # Search for similar products
            search_results = self.vector_engine.search(search_query, k=limit + 1)  # +1 to exclude current product
            
            similar_products = []
            current_product_id = str(product_data['_id'])
            
            for product, score in search_results:
                if str(product['_id']) != current_product_id:  # Exclude current product
                    product_response = ProductResponse(
                        product_id=str(product['_id']),
                        name=product['name'],
                        description=product['description'],
                        category=product['category'],
                        subcategory=product['subcategory'],
                        price=float(product['price']),
                        currency=product['currency'],
                        seller=product['seller'],
                        brand=product['brand'],
                        rating=float(product['rating']),
                        reviews_count=int(product['reviews_count']),
                        in_stock=bool(product['in_stock']),
                        stock_quantity=int(product['stock_quantity']),
                        tags=product['tags'],
                        specifications=product['specifications'],
                        relevance_score=score,
                        free_shipping=product.get('free_shipping', False)
                    )
                    similar_products.append(product_response)
                
                if len(similar_products) >= limit:
                    break
            
            return similar_products
            
        except Exception as e:
            logger.error(f"Get similar products failed: {e}")
            return []
    
    async def _get_suggested_filters(
        self,
        search_results: List[Tuple[Dict[str, Any], float]]
    ) -> Dict[str, List[str]]:
        """Get suggested filters based on search results"""
        
        try:
            categories = set()
            brands = set()
            price_ranges = []
            
            for product, _ in search_results:
                categories.add(product.get('category', ''))
                brands.add(product.get('brand', ''))
                price_ranges.append(float(product.get('price', 0)))
            
            # Create price range suggestions
            if price_ranges:
                min_price = min(price_ranges)
                max_price = max(price_ranges)
                price_suggestions = [
                    f"Under ${int(min_price + (max_price - min_price) * 0.3)}",
                    f"${int(min_price + (max_price - min_price) * 0.3)} - ${int(min_price + (max_price - min_price) * 0.7)}",
                    f"Over ${int(min_price + (max_price - min_price) * 0.7)}"
                ]
            else:
                price_suggestions = []
            
            return {
                "categories": list(categories)[:2],
                "brands": list(brands)[:2],
                "price_ranges": price_suggestions
            }
            
        except Exception as e:
            logger.error(f"Get suggested filters failed: {e}")
            return {}
    
    async def _get_related_searches(self, query: str) -> List[str]:
        """Get related search suggestions"""
        
        try:
            # Simple related searches based on common patterns
            related = [
                f"{query} reviews",
                f"best {query}",
                f"cheap {query}",
                f"{query} deals",
                f"{query} sale"
            ]
            
            return related[:3]  # Return top 3
            
        except Exception as e:
            logger.error(f"Get related searches failed: {e}")
            return []
    
    async def _get_trending_searches(self) -> List[str]:
        """Get trending search queries"""
        
        try:
            # Static trending searches for now
            # In production, this would be based on actual search analytics
            trending = [
                "smartphone",
                "laptop",
                "headphones",
                "sneakers",
                "coffee maker",
                "fitness tracker"
            ]
            
            return trending[:2]
            
        except Exception as e:
            logger.error(f"Get trending searches failed: {e}")
            return []
    
    def refresh_search_index(self):
        """Refresh the FAISS search index"""
        self.vector_engine.refresh_index()


# Service instance
ecommerce_service = EcommerceService()