from pydantic import BaseModel, Field
from typing import Dict, Optional

# ===================
# TENANT DATA MODELS
# ===================

class TenantConfig(BaseModel):
    """
    Schema for a tenant's full configuration.
    Includes branding, layout, and feature flags.
    """
    logo: str = Field(..., example="https://placehold.co/100x50?text=Tenant", description="URL for tenant's logo")
    primaryColor: str = Field(..., example="#2563eb", description="Primary theme color for tenant UI")
    secondaryColor: str = Field(..., example="#a21caf", description="Secondary theme color for tenant UI")
    brandName: str = Field(..., example="Mint core", description="Brand Name for the tenant")
    layout: str = Field(..., example="side", description="Layout type: 'side' or 'top'")
    features: Dict[str, bool] = Field(default_factory=dict, description="Feature flags for this tenant (feature_name: enabled)")

class TenantCreateRequest(BaseModel):
    """
    Request model for creating a new tenant.
    Any field not provided will use a backend default value.
    """
    tenant: str = Field(..., example="tenant4", description="Unique tenant key/identifier")
    primaryColor: Optional[str] = Field(None, example="#2563eb", description="Primary theme color (optional)")
    secondaryColor: Optional[str] = Field(None, example="#a21caf", description="Secondary theme color (optional)")
    brandName: Optional[str] = Field(None, example="Mint core", description="Brand Name for the tenant (optional)")
    logo: Optional[str] = Field(None, example="https://placehold.co/100x50?text=Tenant", description="Logo URL (optional)")
    layout: Optional[str] = Field(None, example="side", description="Navigation layout type (optional)")
    features: Optional[Dict[str, bool]] = Field(None, example={
        "feature1": True,
        "feature2": False
    }, description="Initial feature flags (optional)")

class FeatureUpdateRequest(BaseModel):
    """
    Request model for updating feature flags for a tenant.
    Allows flexible updates to any number of features by name.
    """
    features: Dict[str, bool] = Field(..., example={
        "feature1": False,
        "featureX": True
    }, description="Features to update (feature_name: enabled/disabled)")

class FeatureUpdateResponse(BaseModel):
    message: str
    features: Dict[str, bool]


class TenantConfigResponse(BaseModel):
    """
    Standard response after successful tenant creation.
    """
    message: str = Field(..., example="Tenant created successfully.", description="Success message")
    tenant: TenantConfig = Field(..., description="Created tenant configuration")

class ErrorResponse(BaseModel):
    """
    Standard error response for consistent error handling and docs.
    """
    detail: str = Field(..., example="Tenant not found.", description="Error message")
