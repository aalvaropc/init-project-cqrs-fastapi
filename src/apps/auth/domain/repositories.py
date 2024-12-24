from abc import ABC, abstractmethod

class IAuthRepository(ABC):
    @abstractmethod
    def verify_user_credentials(self, email: str, plain_password: str) -> int:
        """
        Devuelve el user_id si las credenciales son válidas, 
        o None/raise si no lo son.
        """
        pass
