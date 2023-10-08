


def _user_is_staff(user) -> bool:
    """ return True if user is authenticated and staff """

    return user.is_authenticated and user.is_staff