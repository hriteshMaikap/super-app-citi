"""
Authentication routes for the Super App
Banking-grade security with comprehensive logging
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import logging

# Setup logging
logger = logging.getLogger(__name__)

from ..core.database import get_db
from ..schemas.user import UserCreate, UserLogin, UserResponse
from ..schemas.auth import Token, LoginResponse, RegisterResponse, RefreshToken
from ..auth.service import auth_service
from ..auth.dependencies import get_current_user, get_client_info
from ..models.user import User
from ..core.security import security

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> RegisterResponse:
    """
    Register a new user with banking-grade security
    
    - **email**: Valid email address (unique)
    - **username**: Alphanumeric username (unique)
    - **password**: Strong password meeting banking requirements
    - **first_name**: User's first name (encrypted in storage)
    - **last_name**: User's last name (encrypted in storage)
    - **phone**: Valid phone number (encrypted in storage)
    """
    logger.info(f"Registration attempt for user: {user_data.email}")
    try:
        client_info = get_client_info(request)
        logger.info("Got client info, attempting to register user")
        
        result = await auth_service.register_user(user_data, db)
        logger.info(f"Successfully registered user: {user_data.email}")
        
        return result
        
    except ValueError as e:
        logger.error(f"Registration validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Registration failed with unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    """
    Authenticate user and create secure session
    
    - **email**: Registered email address
    - **password**: User's password
    
    Returns access token, refresh token, and user information
    """
    try:
        client_info = get_client_info(request)
        
        result = await auth_service.authenticate_user(
            login_data,
            db,
            device_info=client_info.get("user_agent"),
            ip_address=client_info.get("ip_address")
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again."
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshToken,
    db: AsyncSession = Depends(get_db)
) -> Token:
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Valid refresh token
    """
    try:
        result = await auth_service.refresh_access_token(
            refresh_data.refresh_token,
            db
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/logout")
async def logout(
    refresh_data: RefreshToken,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Logout user by invalidating session
    
    - **refresh_token**: Valid refresh token
    """
    try:
        success = await auth_service.logout_user(refresh_data.refresh_token, db)
        
        if success:
            return {"message": "Logged out successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid refresh token"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get current user profile information
    
    Requires valid access token in Authorization header
    """
    # Decrypt sensitive data for response
    user_data = {
        "id": current_user.id,
        "user_id": current_user.user_id,
        "email": current_user.email,
        "username": current_user.username,
        "first_name": security.decrypt_sensitive_data(current_user.first_name_encrypted),
        "last_name": security.decrypt_sensitive_data(current_user.last_name_encrypted),
        "phone": security.decrypt_sensitive_data(current_user.phone_encrypted),
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "kyc_status": current_user.kyc_status,
        "created_at": current_user.created_at
    }
    
    return UserResponse(**user_data)


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for authentication service"""
    return {"status": "healthy", "service": "authentication"}