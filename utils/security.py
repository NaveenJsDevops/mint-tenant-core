import logging
from fastapi import Request, HTTPException, status, Depends
from firebase_client import firebase_auth, db

# --- Setup Logging ---
logger = logging.getLogger("MintTenantCore.Security")

def get_current_user(request: Request) -> dict:
    """
    Dependency for FastAPI endpoints:
    Verifies the Firebase ID token from the 'Authorization' header,
    fetches user metadata from Firestore, and returns a unified user dict.

    Raises:
        HTTPException: 401 if token is invalid/missing,
        403 if user metadata is missing in Firestore.
    Returns:
        dict: {uid, email, role, tenant}
    """
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("Authorization header missing or invalid")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing or invalid")
    id_token = auth_header.split(" ")[1]
    try:
        decoded = firebase_auth.verify_id_token(id_token)
        user_doc = db.collection("users").document(decoded["uid"]).get()
        user_data = user_doc.to_dict() if user_doc.exists else {}
        if not user_data.get("role") or not user_data.get("tenant"):
            logger.warning(f"User {decoded['uid']} missing role or tenant in Firestore.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User role or tenant not set in Firestore.")
        logger.info(f"Authenticated user: {decoded['uid']} ({user_data.get('role')} @ {user_data.get('tenant')})")
        return {
            "uid": decoded["uid"],
            "email": decoded.get("email"),
            "role": user_data.get("role"),
            "tenant": user_data.get("tenant")
        }
    except Exception as exc:
        logger.error(f"Firebase token verification failed: {exc}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired Firebase token")

def require_role(allowed_roles):
    """
    Dependency factory for RBAC:
    Returns a dependency that allows only specified roles.

    Usage:
        @router.get("/endpoint")
        async def handler(..., current_user=Depends(require_role(["Admin", "HR"]))):
            ...
    """
    def role_dependency(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            logger.warning(f"Access denied: {current_user['role']} not in {allowed_roles}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: requires role(s) {allowed_roles}"
            )
        return current_user
    return role_dependency
