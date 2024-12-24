class UserError(Exception):
    """Excepción base para el dominio de usuarios."""
    pass

class UserCreationError(UserError):
    """Excepción para errores al crear un usuario."""
    pass

class UserUpdateError(UserError):
    """Excepción para errores al actualizar un usuario."""
    pass

class UserDeletionError(UserError):
    """Excepción para errores al eliminar un usuario."""
    pass

class UserAlreadyExistsException(UserCreationError):
    """Excepción para cuando un usuario ya existe."""
    pass

class UserNotFoundException(Exception):
    """Excepción lanzada cuando no se encuentra un usuario."""
    pass