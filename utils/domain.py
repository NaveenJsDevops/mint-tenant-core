# utils/domain.py
from requests import Request

def extract_tenant(request: Request):
    host = request.headers.get("host") or ""
    subdomain = host.split(".")[0]
    return subdomain
