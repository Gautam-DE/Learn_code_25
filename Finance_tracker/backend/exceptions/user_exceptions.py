class UserNotFoundError(Exception):
    def __init__(self, user_id: str):
        super().__init__(f"User with id '{user_id}' not found.")
        self.user_id = user_id


class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists.")
        self.email = email
