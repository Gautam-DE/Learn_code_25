class ValidationError(Exception):
    """Raised when user input is invalid."""


def validate_location_input(location: str) -> str:
    cleaned = location.strip()

    if not cleaned:
        raise ValidationError("Location cannot be empty.")

    if len(cleaned) < 2:
        raise ValidationError("Location must be at least 2 characters long.")

    if len(cleaned) > 200:
        raise ValidationError("Location is too long. Maximum is 200 characters.")

    return cleaned
