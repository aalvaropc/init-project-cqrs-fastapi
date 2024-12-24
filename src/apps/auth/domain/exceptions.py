# src/apps/auth/domain/exceptions.py

class AuthError(Exception):
    """Excepción base para el dominio de autenticación."""
    pass

class AuthenticationError(AuthError):
    """Excepción para errores de autenticación."""
    pass

class AuthorizationError(AuthError):
    """Excepción para errores de autorización."""
    pass

class UserNotFoundError(AuthError):
    """Excepción para cuando el usuario no se encuentra."""
    pass

class InvalidTokenError(AuthError):
    """Excepción para tokens JWT inválidos."""
    pass

class TokenBlacklistError(AuthError):
    """Excepción para errores relacionados con la lista negra de tokens."""
    pass

class InvalidCredentialsException(AuthError):
    """Excepción para credenciales inválidas."""
    pass