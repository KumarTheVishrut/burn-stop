from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
import uuid
from datetime import datetime

from models.user import UserCreate, UserLogin, User, Token
from utils.security import get_password_hash, verify_password, create_access_token, verify_token
from utils.redis_db import redis_db

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    # Check if user already exists
    existing_users = []
    user_keys = []
    
    # Get all user keys to check for existing email
    try:
        # In a real Redis setup, you'd use SCAN, but for simplicity we'll use a user index
        pass
    except:
        pass
    
    # Check if email exists by trying a simple key pattern
    user_id = str(uuid.uuid4())
    user_key = f"user:{user_id}"
    
    # For email uniqueness, we'll use email as a separate key
    email_key = f"email:{user.email}"
    if redis_db.exists(email_key):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user data
    user_data = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_password,
        "organizations": [],
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Save user
    redis_db.set(user_key, user_data)
    redis_db.set(email_key, user_id)  # Email -> user_id mapping
    
    # Create access token
    access_token = create_access_token(data={"sub": user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    # Get user by email
    email_key = f"email:{user_login.email}"
    user_id = redis_db.get(email_key)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_key = f"user:{user_id}"
    user_data = redis_db.get(user_key)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(user_login.password, user_data["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(data={"sub": user_id})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(security)):
    """Dependency to get current user from JWT token"""
    user_id = verify_token(token.credentials)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_key = f"user:{user_id}"
    user_data = redis_db.get(user_key)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="User not found")
    
    return User(**user_data)
