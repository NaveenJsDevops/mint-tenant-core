from fastapi import HTTPException, status
from services.tenant_service import (
    create_tenant,
    get_tenant_config,
    update_tenant_config,
    get_tenant_features,
    update_tenant_features
)

async def create_tenant_controller(
        tenant: str,
        primaryColor: str,
        secondaryColor: str,
        logo: str,
        layout: str,
        brandName: str,
        features: dict = None
) -> dict:
    """
    Create a new tenant with provided configuration and features.
    Returns:
        dict: Success message and the created tenant config.
    Raises:
        HTTPException: 409 if tenant already exists, 400 for other errors.
    """
    try:
        config = create_tenant(tenant, primaryColor, secondaryColor, logo, brandName, layout, features)
        return {
            "message": f"Tenant '{tenant}' created successfully.",
            "tenant": config
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT if "exists" in str(e).lower() else status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create tenant '{tenant}': {e}"
        )

async def get_config_controller(tenant: str) -> dict:
    """
    Retrieve the configuration for the specified tenant.
    Raises:
        HTTPException: 404 if tenant does not exist.
    """
    config = get_tenant_config(tenant)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant '{tenant}' not found."
        )
    return config

async def update_config_controller(tenant: str, updates: dict) -> dict:
    """
    Update configuration for the specified tenant.
    Returns updated tenant config.
    Raises:
        HTTPException: 404 if tenant does not exist.
    """
    try:
        updated = update_tenant_config(tenant, updates)
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to update config for tenant '{tenant}': {e}"
        )

async def get_features_controller(tenant: str) -> dict:
    """
    Retrieve enabled/disabled features for the specified tenant.
    Raises:
        HTTPException: 404 if tenant does not exist.
    """
    try:
        features = get_tenant_features(tenant)
        return features
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not fetch features for tenant '{tenant}': {e}"
        )

async def update_features_controller(tenant: str, features_update: dict) -> dict:
    """
    Update the feature flags for the specified tenant.
    Returns:
        dict: Success message and updated features.
    Raises:
        HTTPException: 404 if tenant does not exist.
    """
    try:
        updated = update_tenant_features(tenant, features_update)
        return {
            "message": f"Features updated successfully for tenant '{tenant}'.",
            "features": updated
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to update features for tenant '{tenant}': {e}"
        )
