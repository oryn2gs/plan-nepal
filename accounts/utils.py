from typing import Dict, Any
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def verify_token(user: Dict[str, Any], token:str) -> bool:
    """ Checks if the verification token is valid.

    Args:
        user (Dict[str, Any]): User object
        token (str): Verification token

    Returns:
        bool: True if valid or False
    """
    
    verification_token = PasswordResetTokenGenerator()
    
    return verification_token.check_token(user, token)