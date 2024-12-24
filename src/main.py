from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.apps.users.infrastructure.routers import router as users_router
from src.apps.auth.infrastructure.routers import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(title="Prueba Init Hexagonal CQRS", version="0.1.0")
    
    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Routers
    app.include_router(users_router)
    app.include_router(auth_router)
    
    return app

app = create_app()