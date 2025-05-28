"""
E-commerce models for product search and management
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from ..core.database import Base


class SearchQuery(Base):
    """
    Track user search queries for analytics and improvements
    """
    __tablename__ = "search_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), index=True)  # Optional - for logged in users
    query_text = Column(Text, nullable=False)
    results_count = Column(Integer, default=0)
    click_position = Column(Integer)  # Which result was clicked
    clicked_product_id = Column(String(50))  # MongoDB product ID
    session_id = Column(String(100))
    
    # Search metadata
    search_type = Column(String(20), default="semantic")  # semantic, text, filter
    response_time_ms = Column(Float)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductView(Base):
    """
    Track product views for recommendation and analytics
    """
    __tablename__ = "product_views"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), index=True)  # Optional
    product_id = Column(String(50), nullable=False)  # MongoDB product ID
    session_id = Column(String(100))
    
    # View metadata
    view_duration_seconds = Column(Integer)
    referrer = Column(String(200))
    device_type = Column(String(20))  # mobile, desktop, tablet
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserWishlist(Base):
    """
    User wishlist/favorites for products
    """
    __tablename__ = "user_wishlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    product_id = Column(String(50), nullable=False)  # MongoDB product ID
    
    # Metadata
    added_from = Column(String(50))  # search, product_page, recommendation
    notes = Column(Text)  # User's personal notes
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Ensure unique wishlist items per user
    __table_args__ = (
        {"mysql_collate": "utf8mb4_unicode_ci"},
    )