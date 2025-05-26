"""
Authentication service with banking-grade security
User registration, login, and session management
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import logging

# Setup logging
logger = logging.getLogger(__name__)

from ..models.user import User, UserSession
from ..schemas.user import UserCreate, UserLogin
from ..schemas.auth import Token, LoginResponse, RegisterResponse
from ..core.security import security
from ..core.config import settings


class AuthService:
    """Banking-grade authentication service"""
    
    @staticmethod
    async def register_user(user_data: UserCreate, db: AsyncSession) -> RegisterResponse:
        """Register new user with encrypted PII storage"""
        logger.info("Starting user registration process")
        
        # Check if user exists
        logger.debug(f"Checking if user exists: {user_data.email}")
        try:
            existing_user = await db.execute(
                select(User).where(
                    (User.email == user_data.email) | 
                    (User.username == user_data.username)
                )
            )
            if existing_user.scalars().first():
                logger.warning(f"User already exists: {user_data.email}")
                raise ValueError("User with this email or username already exists")
            
            logger.debug("Creating new user with encrypted data")
            # Create user with encrypted sensitive data
            user_id = str(uuid.uuid4())
            password_hash = security.hash_password(user_data.password)
            
            # Encrypt PII
            first_name_encrypted = security.encrypt_sensitive_data(user_data.first_name)
            last_name_encrypted = security.encrypt_sensitive_data(user_data.last_name)
            phone_encrypted = security.encrypt_sensitive_data(user_data.phone)
            
            logger.debug(f"Creating user record with ID: {user_id}")
            db_user = User(
                user_id=user_id,
                email=user_data.email,
                username=user_data.username,
                password_hash=password_hash,
                first_name_encrypted=first_name_encrypted,
                last_name_encrypted=last_name_encrypted,
                phone_encrypted=phone_encrypted,
            )
            
            # Add to session and commit
            logger.debug("Adding user to database session")
            db.add(db_user)
            logger.debug("Committing transaction")
            await db.commit()
            logger.debug("Refreshing user object")
            await db.refresh(db_user)
            
            # Create response object
            logger.info(f"User registered successfully: {user_data.email}")
            return RegisterResponse(
                message="User registered successfully",
                user=AuthService._create_user_response(db_user)
            )
        except Exception as e:
            logger.error(f"Error in register_user: {str(e)}", exc_info=True)
            await db.rollback()
            raise
    
    @staticmethod
    async def authenticate_user(
        login_data: UserLogin, 
        db: AsyncSession,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> LoginResponse:
        """Authenticate user and create session"""
        
        # Get user
        result = await db.execute(select(User).where(User.email == login_data.email))
        user = result.scalars().first()
        
        if not user:
            raise ValueError("Invalid credentials")
        
        # Check failed login attempts (banking security)
        if user.failed_login_attempts >= 5:
            raise ValueError("Account locked due to too many failed attempts")
        
        # Verify password
        if not security.verify_password(login_data.password, user.password_hash):
            # Increment failed attempts
            user.failed_login_attempts += 1
            await db.commit()
            raise ValueError("Invalid credentials")
        
        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.last_login = datetime.utcnow()
        
        # Create tokens
        token_data = {"sub": user.user_id, "email": user.email}
        access_token = security.create_access_token(token_data)
        refresh_token = security.create_refresh_token(token_data)
        
        # Create session
        refresh_token_hash = security.hash_password(refresh_token)
        session = UserSession(
            user_id=user.user_id,
            refresh_token_hash=refresh_token_hash,
            device_info=security.encrypt_sensitive_data(device_info or ""),
            ip_address=ip_address,
            expires_at=datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        )
        
        db.add(session)
        await db.commit()
        
        # Prepare response with decrypted data
        user_response = {
            "id": user.id,
            "user_id": user.user_id,
            "email": user.email,
            "username": user.username,
            "first_name": security.decrypt_sensitive_data(user.first_name_encrypted),
            "last_name": security.decrypt_sensitive_data(user.last_name_encrypted),
            "phone": security.decrypt_sensitive_data(user.phone_encrypted),
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "kyc_status": user.kyc_status
        }
        
        tokens = Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.access_token_expire_minutes * 60
        )
        
        return LoginResponse(
            message="Login successful",
            user=user_response,
            tokens=tokens
        )
    
    @staticmethod
    async def refresh_access_token(refresh_token: str, db: AsyncSession) -> Token:
        """Refresh access token using refresh token"""
        
        # Verify refresh token
        payload = security.verify_token(refresh_token, "refresh")
        if not payload:
            raise ValueError("Invalid refresh token")
        
        user_id = payload.get("sub")
        
        # Check if session exists and is active
        session_result = await db.execute(
            select(UserSession).where(
                (UserSession.user_id == user_id) &
                (UserSession.is_active == True) &
                (UserSession.expires_at > datetime.utcnow())
            )
        )
        
        sessions = session_result.scalars().all()
        valid_session = None
        
        for session in sessions:
            if security.verify_password(refresh_token, session.refresh_token_hash):
                valid_session = session
                break
        
        if not valid_session:
            raise ValueError("Invalid refresh token")
        
        # Update session last used
        valid_session.last_used = datetime.utcnow()
        
        # Create new access token
        token_data = {"sub": user_id, "email": payload.get("email")}
        new_access_token = security.create_access_token(token_data)
        
        await db.commit()
        
        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token,  # Keep same refresh token
            expires_in=settings.access_token_expire_minutes * 60
        )
    
    @staticmethod
    async def logout_user(refresh_token: str, db: AsyncSession) -> bool:
        """Logout user by invalidating session"""
        
        payload = security.verify_token(refresh_token, "refresh")
        if not payload:
            return False
        
        user_id = payload.get("sub")
        
        # Deactivate session
        result = await db.execute(
            select(UserSession).where(UserSession.user_id == user_id)
        )
        
        sessions = result.scalars().all()
        for session in sessions:
            if security.verify_password(refresh_token, session.refresh_token_hash):
                session.is_active = False
                break
        
        await db.commit()
        return True
    
    @staticmethod
    def _create_user_response(db_user: User) -> Dict[str, Any]:
        """Create user response object with decrypted sensitive data"""
        return {
            "id": db_user.id,
            "user_id": db_user.user_id,
            "email": db_user.email,
            "username": db_user.username,
            "first_name": security.decrypt_sensitive_data(db_user.first_name_encrypted),
            "last_name": security.decrypt_sensitive_data(db_user.last_name_encrypted),
            "phone": security.decrypt_sensitive_data(db_user.phone_encrypted),
            "is_active": db_user.is_active,
            "is_verified": db_user.is_verified,
            "kyc_status": db_user.kyc_status,
            "created_at": db_user.created_at
        }


# Service instance
auth_service = AuthService()