"""
E-commerce schemas for product search and management
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ProductSearchRequest(BaseModel):
    """Product search request"""
    query: str = Field(..., min_length=1, max_length=200, description="Search query for products")
    limit: int = Field(default=5, ge=1, le=50, description="Number of results to return")
    category_filter: Optional[str] = Field(None, description="Filter by category")
    price_min: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    price_max: Optional[float] = Field(None, ge=0, description="Maximum price filter")
    brand_filter: Optional[str] = Field(None, description="Filter by brand")
    in_stock_only: bool = Field(default=True, description="Show only in-stock products")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating filter")


class ProductResponse(BaseModel):
    """Individual product response"""
    product_id: str
    name: str
    description: str
    category: str
    subcategory: str
    price: float
    currency: str
    seller: str
    brand: str
    rating: float
    reviews_count: int
    in_stock: bool
    stock_quantity: int
    tags: List[str]
    specifications: Dict[str, Any]
    relevance_score: Optional[float] = Field(None, description="Semantic similarity score")
    
    # Display fields
    image_url: Optional[str] = None
    discount_percentage: Optional[float] = None
    free_shipping: Optional[bool] = None
    estimated_delivery: Optional[str] = None


class ProductSearchResponse(BaseModel):
    """Product search response"""
    query: str
    total_results: int
    search_time_ms: float
    products: List[ProductResponse]
    
    # Search metadata
    search_id: str
    applied_filters: Dict[str, Any]
    suggested_filters: Dict[str, List[str]]
    
    # Recommendations
    related_searches: List[str] = []
    trending_searches: List[str] = []


class ProductDetailRequest(BaseModel):
    """Product detail request"""
    product_id: str = Field(..., description="MongoDB product ID")


class ProductDetailResponse(ProductResponse):
    """Detailed product response"""
    views: int
    sales_count: int
    featured: bool
    warranty_months: int
    returnable: bool
    created_at: datetime
    updated_at: datetime
    
    # Additional details
    similar_products: List[ProductResponse] = []
    also_bought: List[ProductResponse] = []
    recently_viewed: List[ProductResponse] = []


class SearchAnalyticsResponse(BaseModel):
    """Search analytics for admin"""
    total_searches: int
    unique_users: int
    top_queries: List[Dict[str, Any]]
    popular_categories: List[Dict[str, Any]]
    avg_response_time_ms: float
    search_success_rate: float


class WishlistRequest(BaseModel):
    """Add to wishlist request"""
    product_id: str = Field(..., description="MongoDB product ID")
    notes: Optional[str] = Field(None, max_length=500)


class WishlistResponse(BaseModel):
    """Wishlist response"""
    user_id: str
    products: List[ProductResponse]
    total_items: int
    total_value: float
    created_at: datetime


class SearchSuggestionResponse(BaseModel):
    """Search suggestions response"""
    suggestions: List[str]
    trending: List[str]
    categories: List[str]
    brands: List[str]