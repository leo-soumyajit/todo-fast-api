from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

# 1. Register Route
@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    # Check if user already exists
    user_exists = await User.find_one(User.username == user_data.username)
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    email_exists = await User.find_one(User.email == user_data.email)
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and save
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username, 
        email=user_data.email, 
        password_hash=hashed_password
    )
    await new_user.create()
    return UserResponse(id=str(new_user.id), username=new_user.username, email=new_user.email)

# 2. Login Route (Token Generation)
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find user
    user = await User.find_one(User.username == form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create Token
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}