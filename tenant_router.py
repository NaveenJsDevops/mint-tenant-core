from fastapi import Request

def extract_subdomain(request: Request) -> str:
    host = request.headers.get("host", "")
    return host.split(".")[0] if host else "default"
