# A simple mock consent manager to simulate checking user consent.

MOCK_USER_CONSENT = {
    "user_has_consent": True,
    "user_no_consent": False,
    "user_error_state": "error",
}

class ConsentError(Exception):
    """Custom exception for consent failures."""
    pass

def require_consent(user_id: str):
    """
    Checks if a user has given consent.
    Raises ConsentError if consent is not granted or state is unknown.
    """
    if user_id not in MOCK_USER_CONSENT:
        raise ConsentError(f"Consent status for user '{user_id}' is unknown.")
    
    status = MOCK_USER_CONSENT.get(user_id)
    
    if status is not True:
        raise ConsentError(f"Consent denied or in error state for user '{user_id}'.")
    
    return True