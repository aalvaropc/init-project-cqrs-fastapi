from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Decodes the JWT token and retrieves the user ID from the payload.

    Args:
        token (str): The JWT token from the Authorization header.

    Returns:
        dict: A dictionary containing user information.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id}
    except PyJWTError:
        raise credentials_exception