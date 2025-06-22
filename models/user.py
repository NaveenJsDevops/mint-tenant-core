from typing import Optional
from pydantic import BaseModel, Field

# ====================
# USER PROFILE MODELS
# ====================

class UserProfile(BaseModel):
    """
    Model for returning the user's profile info.
    Data is sourced from Firebase Auth (uid, email) and Firestore (role, tenant).
    """
    uid: str = Field(..., example="v1HJ6GQlQOeNk0Bgj6rDkeIoZn12")
    email: Optional[str] = Field(None, example="user@example.com")
    role: str = Field(..., example="HR")
    tenant: str = Field(..., example="tenant1")

class UserProfileUpdateRequest(BaseModel):
    """
    Request schema for admin updating user profile metadata in Firestore.
    """
    uid: str = Field(..., example="v1HJ6GQlQOeNk0Bgj6rDkeIoZn12")
    role: str = Field(..., example="Employee")
    tenant: str = Field(..., example="tenant2")

class SuccessResponse(BaseModel):
    """
    Generic success response model.
    """
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Profile updated successfully.")

class ErrorResponse(BaseModel):
    """
    Standard error response for OpenAPI docs and client-side parsing.
    """
    detail: str = Field(..., example="User not found.")
