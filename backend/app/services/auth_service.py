"""
Authentication Service - Business logic for authentication.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import logging

from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.core.exceptions import AuthenticationError, ValidationError
from app.db.models.user import User, UserSession
from app.schemas.user import UserCreate, UserLogin, Token
from app.cache.cache_manager import CacheManager

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize auth service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.cache = CacheManager()
    
    async def register_user(self, user_data: UserCreate) -> User:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
        
        Returns:
            Created user
        
        Raises:
            ValidationError: If email or username already exists
        """
        # Check if email exists
        email_exists = await self._email_exists(user_data.email)
        if email_exists:
            raise ValidationError("Email already registered")
        
        # Check if username exists
        username_exists = await self._username_exists(user_data.username)
        if username_exists:
            raise ValidationError("Username already taken")
        
        # Hash password
        password_hash = get_password_hash(user_data.password)
        
        # Create user
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=password_hash,
            full_name=user_data.full_name
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info(f"User registered: {user.email}")
        return user
    
    async def authenticate_user(self, credentials: UserLogin) -> User:
        """
        Authenticate user with email and password.
        
        Args:
            credentials: Login credentials
        
        Returns:
            Authenticated user
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        # Get user by email
        user = await self._get_user_by_email(credentials.email)
        
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise AuthenticationError("Account is temporarily locked")
        
        # Verify password
        if not verify_password(credentials.password, user.password_hash):
            await self._handle_failed_login(user)
            raise AuthenticationError("Invalid email or password")
        
        # Check if account is active
        if not user.is_active:
            raise AuthenticationError("Account is inactive")
        
        # Reset failed login attempts
        await self._reset_failed_login_attempts(user)
        
        # Update last login
        user.last_login = datetime.utcnow()
        await self.db.commit()
        
        logger.info(f"User authenticated: {user.email}")
        return user
    
    async def create_tokens(self, user: User) -> Token:
        """
        Create access and refresh tokens for user.
        
        Args:
            user: Authenticated user
        
        Returns:
            Token response with access and refresh tokens
        """
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_token(
            data={"sub": str(user.id), "type": "access"},
            expires_delta=access_token_expires
        )
        
        # Create refresh token
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = self._create_token(
            data={"sub": str(user.id), "type": "refresh"},
            expires_delta=refresh_token_expires
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    async def refresh_access_token(self, refresh_token: str) -> Token:
        """
        Create new access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
        
        Returns:
            New token pair
        
        Raises:
            AuthenticationError: If refresh token is invalid
        """
        try:
            # Decode refresh token
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            user_id = payload.get("sub")
            token_type = payload.get("type")
            
            if token_type != "refresh":
                raise AuthenticationError("Invalid token type")
            
            # Get user
            user = await self.db.get(User, user_id)
            if not user or not user.is_active:
                raise AuthenticationError("User not found or inactive")
            
            # Create new token pair
            return await self.create_tokens(user)
            
        except JWTError:
            raise AuthenticationError("Invalid refresh token")
    
    async def logout_user(self, user_id: str, session_token: Optional[str] = None):
        """
        Logout user and invalidate session.
        
        Args:
            user_id: User ID
            session_token: Optional session token to invalidate
        """
        # Invalidate session if provided
        if session_token:
            result = await self.db.execute(
                update(UserSession)
                .where(UserSession.user_id == user_id)
                .where(UserSession.session_token == session_token)
                .values(is_active=False)
            )
            await self.db.commit()
        
        # Clear user cache
        await self.cache.delete(f"user:{user_id}")
        
        logger.info(f"User logged out: {user_id}")
    
    def _create_token(self, data: Dict[str, Any], expires_delta: timedelta) -> str:
        """Create JWT token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    async def _email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none() is not None
    
    async def _username_exists(self, username: str) -> bool:
        """Check if username already exists."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none() is not None
    
    async def _get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def _handle_failed_login(self, user: User):
        """Handle failed login attempt."""
        user.failed_login_attempts += 1
        
        # Lock account if too many failed attempts
        if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            user.locked_until = datetime.utcnow() + timedelta(
                minutes=settings.LOGIN_ATTEMPT_WINDOW_MINUTES
            )
            logger.warning(f"Account locked due to failed login attempts: {user.email}")
        
        await self.db.commit()
    
    async def _reset_failed_login_attempts(self, user: User):
        """Reset failed login attempts counter."""
        if user.failed_login_attempts > 0:
            user.failed_login_attempts = 0
            user.locked_until = None
            await self.db.commit()
