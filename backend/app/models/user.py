"""
User model with banking-grade security
Encrypted PII storage and audit trails
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from datetime import datetime

from ..core.database import Base  # Import Base from database.py


class User(Base):
    """
    User model with encrypted sensitive data storage
    Banking compliance with audit trails
    """
    __tablename__ = "users"
    
    # Primary identifiers
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), unique=True, index=True)  # UUID
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Profile (encrypted)
    first_name_encrypted = Column(Text)  # Encrypted PII
    last_name_encrypted = Column(Text)   # Encrypted PII
    phone_encrypted = Column(Text)       # Encrypted PII
    
    # Security
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime(timezone=True))
    
    # KYC Status (to be expanded)
    kyc_status = Column(String(20), default="pending")  # pending, verified, rejected
    
    # Audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class UserSession(Base):
    """
    User session management for banking security
    Track active sessions and device information
    """
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), index=True, nullable=False)
    refresh_token_hash = Column(String(255), nullable=False)
    device_info = Column(Text)  # Encrypted device fingerprint
    ip_address = Column(String(45))  # IPv6 compatible
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_used = Column(DateTime(timezone=True), server_default=func.now())