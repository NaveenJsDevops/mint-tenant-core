from fastapi import HTTPException, status, Depends
from utils.security import get_current_user
from services.auth_service import fetch_user_metadata, update_user_metadata

async def get_current_user_profile(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Controller to fetch the current user's profile info (role, tenant, email, uid).

    Returns:
        dict: User's profile from Firestore (or raises 404 if not found).
    """
    user_metadata = fetch_user_metadata(current_user["uid"])
    if not user_metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found in Firestore."
        )
    # Merge Firebase Auth info (email, uid) with Firestore metadata (role, tenant)
    profile = {
        "uid": current_user["uid"],
        "email": current_user.get("email"),
        "role": user_metadata.get("role"),
        "tenant": user_metadata.get("tenant")
    }
    return profile

async def update_user_profile(uid: str, role: str, tenant: str) -> dict:
    """
    Controller to update a user's role or tenant in Firestore.

    Args:
        uid (str): Firebase Authentication user UID.
        role (str): New role for the user.
        tenant (str): New tenant for the user.

    Returns:
        dict: Confirmation message on successful update.
    """
    try:
        update_user_metadata(uid, role, tenant)
        return {"success": True, "message": f"User profile updated for UID {uid}."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user profile: {e}"
        )
