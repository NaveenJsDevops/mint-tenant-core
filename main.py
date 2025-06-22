import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from dotenv import load_dotenv
from starlette.responses import FileResponse

# Load environment variables
load_dotenv()

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("MintTenantCoreApp")

# Config
API_PREFIX = os.getenv("API_PREFIX", "/api")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://tenant1.localhost:3000,http://tenant2.localhost:3000").split(",")
]

# FastAPI app
app = FastAPI(
    title="MintTenantCore Backend",
    description="Multi-Tenant Role-Based Access Control system using FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Static assets
LOGO_DIR = os.path.join(os.getcwd(), "assets")

@app.get("/static/logos/{filename}", tags=["static"])
async def get_logo(filename: str):
    file_path = os.path.join(LOGO_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Logo not found")
    response = FileResponse(file_path, media_type="image/png")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from routers.auth_router import router as auth_router
from routers.tenant_router import router as tenant_router

def register_routers(app: FastAPI):
    app.include_router(auth_router, prefix=f"{API_PREFIX}/auth", tags=["auth"])
    app.include_router(tenant_router, prefix=f"{API_PREFIX}" + "/{tenant}", tags=["tenant"])

register_routers(app)

# Global exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc} | Path: {request.url}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error. Please contact support."})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc} | Path: {request.url}")
    return JSONResponse(status_code=422, content={"detail": exc.errors(), "body": exc.body})

# Health check
@app.get("/ping", tags=["health"])
async def ping():
    logger.info("Health check called")
    return {"message": "pong"}

# Entry point
if __name__ == "__main__":
    try:
        logger.info(f"Starting MintTenantCore on {HOST}:{PORT} with log level {LOG_LEVEL}")
        import uvicorn
        uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    except Exception as exc:
        logger.exception("Failed to start the application.")
        raise exc
