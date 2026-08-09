from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.user import router as user_router

app = FastAPI(
    title="Plataforma Core API",
    description="API principal responsável pelo gerenciamento e materialização de dados do produto.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

origens_permitidas = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)


@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verifica se a API está online e respondendo."""
    return {"status": "ok", "ambiente": "desenvolvimento"}

