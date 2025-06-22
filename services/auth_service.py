from firebase_client import db
from typing import Optional

def fetch_user_metadata(uid: str) -> Optional[dict]:
    """
    Fetch a user's metadata (role, tenant, etc.) from Firestore.

    Args:
        uid (str): Firebase Authentication user UID.

    Returns:
        dict or None: User metadata if exists, otherwise None.

    Raises:
        ValueError: If uid is empty.
        Exception: For unexpected Firestore errors.
    """
    if not uid:
        raise ValueError("User UID must be provided.")
    try:
        doc = db.collection("users").document(uid).get()
        return doc.to_dict() if doc.exists else None
    except Exception as e:
        # Log or handle error as needed
        raise Exception(f"Failed to fetch metadata for user {uid}: {e}")

def update_user_metadata(uid: str, role: str, tenant: str) -> None:
    """
    Update or set a user's metadata (role, tenant) in Firestore.

    Args:
        uid (str): Firebase Authentication user UID.
        role (str): User's role (e.g., 'HR', 'Employee', 'Admin').
        tenant (str): Tenant key the user belongs to.

    Raises:
        ValueError: If any required field is missing.
        Exception: For unexpected Firestore errors.
    """
    if not uid or not role or not tenant:
        raise ValueError("User UID, role, and tenant are required to update metadata.")
    try:
        db.collection("users").document(uid).set({
            "role": role,
            "tenant": tenant
        }, merge=True)
    except Exception as e:
        # Log or handle error as needed
        raise Exception(f"Failed to update metadata for user {uid}: {e}")
