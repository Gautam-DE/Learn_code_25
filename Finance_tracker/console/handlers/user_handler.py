from backend.controllers.user_controller import UserController
from backend.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)


class UserHandler:
    def __init__(self, user_controller: UserController):
        self._controller = user_controller

    def handle_create_user(self) -> None:
        print("\nCreate New User")
        name = input("Name  : ").strip()
        email = input("Email : ").strip()
        try:
            user = self._controller.create_user(name, email)
            print("\nSuccess: User created.")
            print(f"ID    : {user['id']}")
            print(f"Name  : {user['name']}")
            print(f"Email : {user['email']}")
            print("\nNote: Copy your ID as you will need it to log in.")
        except UserAlreadyExistsError as error:
            print(f"\nError: {error}")

    def handle_get_user(self) -> None:
        print("\nUser Details")
        user_id = input("User ID : ").strip()
        try:
            user = self._controller.get_user(user_id)
            print(f"\nName    : {user['name']}")
            print(f"Email   : {user['email']}")
            print(f"Joined  : {user['created_at'][:10]}")
        except UserNotFoundError as error:
            print(f"\nError: {error}")
