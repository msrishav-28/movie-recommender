"""
Security utilities: password hashing, JWT tokens, OAuth.
Production-grade authentication and authorization.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import hashlib

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer for JWT
security = HTTPBearer()


class PasswordHasher:
    """Handle password hashing and verification."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Validate password strength.
        Returns (is_valid, error_message)
        """
        if len(password) < settings.PASSWORD_MIN_LENGTH:
            return False, f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters"
        
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "Password must contain at least one special character"
        
        return True, ""


class JWTHandler:
    """Handle JWT token creation and validation."""
    
    @staticmethod
    def create_access_token(
        subject: str | Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create access token.
        
        Args:
            subject: User identifier or dict of claims
            expires_delta: Token expiration time
        
        Returns:
            Encoded JWT token
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        if isinstance(subject, dict):
            to_encode = subject.copy()
        else:
            to_encode = {"sub": str(subject)}
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(subject: str) -> str:
        """
        Create refresh token with longer expiration.
        
        Args:
            subject: User identifier
        
        Returns:
            Encoded JWT refresh token
        """
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode = {
            "sub": str(subject),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "jti": secrets.token_urlsafe(32)  # JWT ID for revocation
        }
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """
        Decode and validate JWT token.
        
        Args:
            token: JWT token string
        
        Returns:
            Token payload
        
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def verify_token_type(payload: Dict[str, Any], expected_type: str) -> bool:
        """Verify token type (access or refresh)."""
        return payload.get("type") == expected_type
    
    @staticmethod
    def create_email_verification_token(email: str) -> str:
        """Create token for email verification."""
        expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode = {
            "email": email,
            "exp": expire,
            "type": "email_verification"
        }
        
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def create_password_reset_token(email: str) -> str:
        """Create token for password reset."""
        expire = datetime.utcnow() + timedelta(hours=1)
        
        to_encode = {
            "email": email,
            "exp": expire,
            "type": "password_reset"
        }
        
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )


class APIKeyManager:
    """Manage API keys for external access."""
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure API key."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key for storage."""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def verify_api_key(api_key: str, hashed_key: str) -> bool:
        """Verify API key against stored hash."""
        return hashlib.sha256(api_key.encode()).hexdigest() == hashed_key


class RateLimiter:
    """Rate limiting utilities."""
    
    @staticmethod
    def get_rate_limit_key(identifier: str, endpoint: str) -> str:
        """Generate rate limit key for Redis."""
        return f"rate_limit:{identifier}:{endpoint}"
    
    @staticmethod
    def get_rate_limit_window(window_type: str = "minute") -> int:
        """Get rate limit window in seconds."""
        windows = {
            "minute": 60,
            "hour": 3600,
            "day": 86400
        }
        return windows.get(window_type, 60)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependency to get current user ID from JWT token.
    
    Usage:
        @app.get("/protected")
        async def protected_route(user_id: str = Depends(get_current_user_id)):
            ...
    """
    token = credentials.credentials
    payload = JWTHandler.decode_token(token)
    
    if not JWTHandler.verify_token_type(payload, "access"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    return user_id


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[str]:
    """
    Dependency to get current user ID if token provided, None otherwise.
    For endpoints that work with or without authentication.
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user_id(credentials)
    except HTTPException:
        return None


def require_admin():
    """Dependency to require admin role."""
    async def _require_admin(user_id: str = Depends(get_current_user_id)):
        # Check if user is admin (implement your logic)
        # This is a placeholder - you would check against database
        pass
    return _require_admin


def require_premium():
    """Dependency to require premium subscription."""
    async def _require_premium(user_id: str = Depends(get_current_user_id)):
        # Check if user has premium subscription
        # This is a placeholder - you would check against database
        pass
    return _require_premium


# Export commonly used functions
hash_password = PasswordHasher.hash_password
verify_password = PasswordHasher.verify_password
validate_password_strength = PasswordHasher.validate_password_strength
create_access_token = JWTHandler.create_access_token
create_refresh_token = JWTHandler.create_refresh_token
decode_token = JWTHandler.decode_token
create_email_verification_token = JWTHandler.create_email_verification_token
create_password_reset_token = JWTHandler.create_password_reset_token
generate_api_key = APIKeyManager.generate_api_key
