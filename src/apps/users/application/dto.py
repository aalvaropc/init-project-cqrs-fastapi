from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.fields import Field


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    
class UpdateUserRequest(BaseModel):
    name: str = Field(None, title="User's Name", max_length=100, example="John Doe")
    email: EmailStr = Field(None, title="User's Email", example="john.doe@example.com")