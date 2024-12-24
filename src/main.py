from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from src.core.dependency_injection import get_db_reader, get_db_writer
from src.core.security import verify_jwt_token
from src.apps.users.application.commands.create_user_command import publish_create_user_command
from src.apps.users.application.queries.get_user_query import get_user_by_id
from src.apps.users.domain.exceptions import UserNotFoundException
from src.apps.auth.infrastructure.auth_repository import AuthRepository
from src.apps.auth.domain.use_cases import LoginUserUseCase
from src.apps.auth.domain.exceptions import InvalidCredentialsException
from src.apps.auth.infrastructure.jwt_service import JWTService
from src.apps.users.infrastructure.orm_models import UserModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HexagonalCQRSApp")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users", status_code=202)
def create_user(name: str, email: str, password: str, db: Session = Depends(get_db_writer)):
    """
    Publica un comando para crear un usuario (vía RabbitMQ).
    También verifica si el usuario ya existe en la base de datos de escritura.
    """
    # Verificar si el usuario ya existe
    existing_user = db.query(UserModel).filter(UserModel.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    # Publicar el comando
    publish_create_user_command(name, email, password)
    return {"detail": "User creation command published."}

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db_reader)):
    """
    Lectura en la BD de lectura (Replica).
    """
    try:
        user = get_user_by_id(db, user_id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/auth/login")
def login(email: str, password: str, db: Session = Depends(get_db_writer)):
    """
    Login sincrónico para obtener un JWT (usa BD de escritura).
    """
    repo = AuthRepository(db)
    use_case = LoginUserUseCase(repo)

    try:
        user_id = use_case.execute(email, password)
        token = JWTService.generate_token(user_id)
        return {"access_token": token, "token_type": "bearer"}
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))

def get_current_user(authorization: str = Header(None)):
    """
    Dependencia para inyectar el usuario actual a partir de un JWT 
    en la cabecera Authorization: Bearer <token>.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")

    try:
        user_id = verify_jwt_token(token)
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/users/me")
def get_me(current_user_id: int = Depends(get_current_user)):
    """
    Devuelve el ID del usuario autenticado (ejemplo de endpoint protegido).
    """
    return {"user_id": current_user_id}
