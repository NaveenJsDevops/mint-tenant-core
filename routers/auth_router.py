from fastapi import APIRouter, Depends, status
from utils.security import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get(
    "/me",
    summary="Get current authenticated user's profile",
    tags=["auth"],
    response_description="Returns the current user's UID, email, role, and tenant as stored in Firestore."
)
async def get_profile(current_user: dict = Depends(get_current_user)) -> JSONResponse:
    """
    Returns the authenticated user's profile information, including:
    - **uid:** Firebase UID
    - **email:** User's email address (from Firebase Auth)
    - **role:** User's assigned role (from Firestore)
    - **tenant:** Tenant key (from Firestore)
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "uid": current_user.get("uid"),
            "email": current_user.get("email"),
            "role": current_user.get("role"),
            "tenant": current_user.get("tenant"),
        }
    )
