import os
import json
from typing import Dict, Any, Optional
from config import (
    DEFAULT_FEATURE_FLAGS,
    DEFAULT_PRIMARY_COLOR,
    DEFAULT_SECONDARY_COLOR,
    DEFAULT_LOGO,
    DEFAULT_LAYOUT,
    DEFAULT_BRAND_NAME,
)

TENANTS_FILE = os.path.join(os.path.dirname(__file__), "../tenants.json")


def load_tenants() -> Dict[str, Dict[str, Any]]:
    try:
        with open(TENANTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        raise Exception("Corrupted tenants.json file.")


def save_tenants(data: Dict[str, Dict[str, Any]]):
    with open(TENANTS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def create_tenant(
        tenant: str,
        primaryColor: Optional[str] = None,
        secondaryColor: Optional[str] = None,
        logo: Optional[str] = None,
        brandName: Optional[str] = None,
        layout: Optional[str] = None,
        features: Optional[Dict[str, bool]] = None
) -> Dict[str, Any]:
    tenants = load_tenants()

    if tenant in tenants:
        raise Exception("Tenant already exists.")

    config = {
        "features": features if features is not None else DEFAULT_FEATURE_FLAGS.copy(),
        "primaryColor": primaryColor or DEFAULT_PRIMARY_COLOR,
        "secondaryColor": secondaryColor or DEFAULT_SECONDARY_COLOR,
        "logo": logo or DEFAULT_LOGO,
        "brandName": brandName or DEFAULT_BRAND_NAME,
        "layout": layout or DEFAULT_LAYOUT,
    }

    tenants[tenant] = config
    save_tenants(tenants)
    return config


def get_tenant_config(tenant: str) -> Optional[Dict[str, Any]]:
    tenants = load_tenants()
    return tenants.get(tenant)


def update_tenant_config(tenant: str, updates: dict) -> Dict[str, Any]:
    tenants = load_tenants()

    if tenant not in tenants:
        raise Exception("Tenant not found.")

    tenants[tenant].update(updates)
    save_tenants(tenants)
    return tenants[tenant]


def get_tenant_features(tenant: str) -> Dict[str, bool]:
    tenants = load_tenants()

    if tenant not in tenants:
        raise Exception("Tenant not found.")

    return tenants[tenant].get("features", {})


def update_tenant_features(tenant: str, features_update: Dict[str, bool]) -> Dict[str, bool]:
    tenants = load_tenants()

    if tenant not in tenants:
        raise Exception("Tenant not found.")

    current = tenants[tenant].get("features", {})
    current.update(features_update)
    tenants[tenant]["features"] = current

    save_tenants(tenants)
    return current
