from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.core.dependency_injection import get_db_writer
from src.apps.auth.infrastructure.auth_repository import AuthRepository
from src.apps.auth.domain.use_cases import LoginUserUseCase
from src.apps.auth.domain.exceptions import InvalidCredentialsException
from src.apps.auth.infrastructure.jwt_service import JWTService
from src.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db_writer)):
    repo = AuthRepository(db)
    jwt_service = JWTService(
        secret_key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
        expire_minutes=settings.JWT_EXPIRE_MINUTES
    )
    use_case = LoginUserUseCase(repo, jwt_service)
    
    try:
        user_id = use_case.execute(email, password)
        token = jwt_service.generate_token(user_id=user_id, email=email)
        return {"access_token": token, "token_type": "bearer"}
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))