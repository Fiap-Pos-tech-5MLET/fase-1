# ===========================
# auth/schemas/dependencies.py
# ===========================
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .token import TokenData
from ..models.user import User, UserInDB
from .jwt_handler import SECRET_KEY, ALGORITHM
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/oauth_login")

def get_user(username: str):
    try:
        with open("users.json", "r") as f:
            users_db = json.load(f)
        if username in users_db:
            user_dict = users_db[username]
            return UserInDB(**user_dict)
    except FileNotFoundError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
