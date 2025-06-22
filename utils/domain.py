# utils/domain.py
from requests import Request

def extract_subdomain(request: Request) -> str:
    host = request.headers.get("host", "")
    host = host.split(":")[0]  # remove port number
    parts = host.split(".")

    # localhost: tenant1.localhost, tenant2.localhost
    if len(parts) >= 3:
        return parts[0]  # tenant1 / tenant2
    elif host.startswith("localhost") or host.startswith("127.0.0.1"):
        return "default"  # fallback if subdomain missing
    return parts[0]
