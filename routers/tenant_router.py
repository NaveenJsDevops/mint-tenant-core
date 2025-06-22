from typing import Dict
from fastapi import APIRouter, Depends, Path, Request
from models.tenant import (
    TenantCreateRequest, TenantConfig, FeatureUpdateRequest,
    TenantConfigResponse, ErrorResponse
)
from utils.security import require_role, get_current_user
from controllers.tenant_controller import (
    create_tenant_controller,
    get_config_controller,
    update_config_controller,
    get_features_controller,
    update_features_controller
)

router = APIRouter()

@router.post(
    "/create",
    response_model=TenantConfigResponse,
    responses={
        409: {"model": ErrorResponse, "description": "Tenant already exists"},
        400: {"model": ErrorResponse, "description": "Validation error"},
    },
    summary="Create a new tenant (Admin/HR only)",
    tags=["tenant"]
)
async def create_tenant_endpoint(
        body: TenantCreateRequest,
        current_user: dict = Depends(require_role(["Admin", "HR"]))
):
    """
    Create a new tenant with its config.
    """
    return await create_tenant_controller(
        body.tenant,
        body.primaryColor,
        body.secondaryColor,
        body.logo,
        body.brandName,
        body.layout,
        body.features
    )


@router.get("/{tenant}/config")
async def get_config_endpoint(tenant: str, request: Request):
    config = await get_config_controller(tenant)
    if config.get("logo") and not config["logo"].startswith("http"):
        config["logo"] = str(request.base_url).rstrip("/") + config["logo"]
    return config


@router.put(
    "/{tenant}/config",
    response_model=TenantConfig,
    responses={404: {"model": ErrorResponse}},
    summary="Update tenant config (Admin/HR only)",
    tags=["tenant"]
)
async def update_config_endpoint(
        tenant: str,
        updates: TenantCreateRequest,
        current_user: dict = Depends(require_role(["Admin", "HR"]))
):
    return await update_config_controller(tenant, updates.dict(exclude_unset=True))


@router.get(
    "/{tenant}/features",
    response_model=Dict[str, bool],
    responses={404: {"model": ErrorResponse}},
    summary="Get feature flags for a tenant",
    tags=["tenant"]
)
async def get_features_endpoint(
        tenant: str,
        current_user: dict = Depends(get_current_user)
):
    return await get_features_controller(tenant)


@router.put(
    "/{tenant}/features",
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Update features for a tenant (HR/Admin only)",
    tags=["tenant"]
)
async def update_features_endpoint(
        tenant: str,
        body: FeatureUpdateRequest,
        current_user: dict = Depends(require_role(["HR", "Admin"]))
):
    return await update_features_controller(tenant, body.features)
