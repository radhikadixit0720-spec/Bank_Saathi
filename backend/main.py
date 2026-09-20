"""
Bank Saathi API - application entrypoint.

Run locally with:
    uvicorn backend.main:app --reload --port 8000

The app is organised as:
    config/     environment-driven settings
    database/   MongoDB connection (with safe in-memory fallback)
    schemas/    Pydantic request/response models
    services/   business logic, independent of FastAPI
    routes/     thin HTTP routers that call into services/
    data/       static/configurable reference data (templates, checklists, branches)
    utils/      small shared helpers (ids, error formatting)
"""
import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config.settings import settings
from backend.database.mongo import close_mongo_connection, connect_to_mongo, is_using_fallback
from backend.routes import (
    checklist,
    customer,
    employee,
    error_checker,
    form_scanner,
    language,
    legacy,
    requests,
    tokens,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bank_saathi")

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# CORS: only the origins listed in ALLOWED_ORIGINS (env var) may call this
# API from a browser. Configure this before deploying anywhere public.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return clean, readable validation errors instead of a raw traceback."""
    errors = [
        {"field": ".".join(str(p) for p in e["loc"][1:]), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Please check the highlighted fields.", "errors": errors},
    )


@app.on_event("startup")
async def on_startup():
    connect_to_mongo()


@app.on_event("shutdown")
async def on_shutdown():
    close_mongo_connection()


@app.get("/")
def root():
    return {
        "status": "Bank Saathi API is running",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "database": "in_memory_fallback" if is_using_fallback() else "mongodb",
    }


@app.get("/health")
def health():
    return {"status": "ok", "database": "in_memory_fallback" if is_using_fallback() else "mongodb"}


# --- Feature routers --------------------------------------------------
app.include_router(form_scanner.router)
app.include_router(language.router)
app.include_router(checklist.router)
app.include_router(error_checker.router)
app.include_router(requests.router)
app.include_router(tokens.router)
app.include_router(employee.router)
app.include_router(customer.router)

# --- Legacy prototype endpoints (kept for backward compatibility) -----
app.include_router(legacy.router)
