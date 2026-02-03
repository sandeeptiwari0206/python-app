from fastapi import APIRouter, HTTPException 
from passlib.context import CryptContext 
from database import users_collection 
from models import User 
 
router = APIRouter() 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
 
def hash_password(password: str): 
    return pwd_context.hash(password) 
 
@router.post("/register") 
def register(user: User): 
    if users_collection.find_one({"email": user.email}): 
        raise HTTPException(status_code=400, detail="User already exists") 
 
    users_collection.insert_one({ 
        "username": user.username, 
        "email": user.email, 
        "password": hash_password(user.password) 
    }) 
 
    return {"message": "User registered successfully"}
