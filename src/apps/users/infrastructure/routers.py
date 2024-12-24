from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.dependency_injection import get_db_reader, get_db_writer
from src.apps.users.application.commands.create_user_command import publish_create_user_command
from src.apps.users.application.commands.update_user_command import publish_update_user_command
from src.apps.users.application.commands.delete_user_command import publish_delete_user_command
from src.apps.users.application.queries.get_user_query import get_user_by_id
from src.apps.users.domain.exceptions import UserNotFoundException
from src.apps.users.infrastructure.orm_models import UserModel
from src.apps.users.application.dto import CreateUserRequest, UpdateUserRequest
from src.core.security import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=202, summary="Create a new user")
def create_user(request: CreateUserRequest, db: Session = Depends(get_db_writer)):
    """
    Creates a new user by publishing a command to RabbitMQ.

    Args:
        request (CreateUserRequest): The user data (name, email, password).
        db (Session): Database session for validation.

    Returns:
        dict: A confirmation message indicating the creation command was published.
    """
    existing_user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    publish_create_user_command(request.name, request.email, request.password)
    return {"detail": "User creation command published."}


@router.get("/{user_id}", summary="Get user details by ID")
def get_user_details(user_id: int, db: Session = Depends(get_db_reader)):
    """
    Retrieves the details of a user by their ID.

    Args:
        user_id (int): The ID of the user.
        db (Session): Database session for querying user details.

    Returns:
        dict: The user's details (ID, name, email).
    """
    try:
        user = get_user_by_id(db, user_id)
        return {"id": user.id, "name": user.name, "email": user.email}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/me", status_code=202, summary="Update authenticated user's profile")
def update_authenticated_user(
    request: UpdateUserRequest,
    current_user: dict = Depends(get_current_user),  # Cambiado de `int` a `dict`
):
    """
    Updates the profile of the currently authenticated user.

    Args:
        request (UpdateUserRequest): The updated user data (name, email).
        current_user (dict): The authenticated user's data.

    Returns:
        dict: A confirmation message.
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user data.")

    if not request.name and not request.email:
        raise HTTPException(status_code=400, detail="No update fields provided.")

    publish_update_user_command(
        user_id=user_id,
        name=request.name,
        email=request.email,
    )
    return {"detail": "User profile update command published."}

# @router.delete("/me", status_code=202, summary="Delete authenticated user")
# def delete_authenticated_user(current_user_id: int = Depends(get_current_user)):
#     """
#     Deletes the authenticated user's account by publishing a command to RabbitMQ.

#     Args:
#         current_user_id (int): The ID of the authenticated user.

#     Returns:
#         dict: Confirmation of the delete command.
#     """
#     publish_delete_user_command(user_id=current_user_id)
#     return {"detail": "User delete command published."}
