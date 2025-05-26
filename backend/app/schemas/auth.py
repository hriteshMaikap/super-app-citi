"""
Authentication schemas for JWT and session management
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token payload data"""
    user_id: Optional[str] = None
    email: Optional[str] = None


class RefreshToken(BaseModel):
    """Refresh token request"""
    refresh_token: str


class LoginResponse(BaseModel):
    """Login success response"""
    message: str
    user: dict
    tokens: Token


class RegisterResponse(BaseModel):
    """Registration success response"""
    message: str
    user: dict