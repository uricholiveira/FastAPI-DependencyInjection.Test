PASSWORD_REGEX = "((?=.*)(?=.*[a-z])(?=.*[A-Z])(?=.*).{8,64})"


def validate_password(value):
    password = value
    min_length = 8
    errors = ''
    if len(password) < min_length:
        errors += 'Password must be at least 8 characters long. '
    if not any(character.islower() for character in password):
        errors += 'Password should contain at least one lowercase character.'
    if errors:
        raise ValueError(errors)

    return value
