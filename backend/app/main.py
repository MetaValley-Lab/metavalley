import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.startup import router as startup_router
from app.api.chat import router as agents_router
from app.api.planning_item import router as planning_item_router
from app.api.canvas_zone import router as canvas_zone_router
from app.api.product import router as product_router
from app.api.simulation_interest import router as simulation_interest_router

from app.core.limiter import limiter

AMBIENTE = os.getenv("APP_ENV", "development").lower()
EM_PRODUCAO = AMBIENTE == "production"

ORIGENS_PERMITIDAS = [
    origem.strip()
    for origem in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:3000"
    ).split(",")
    if origem.strip()
]

app = FastAPI(
    title="Plataforma Core API",
    description="API principal responsável pelo gerenciamento e materialização de dados do produto.",
    version="1.0.0",
    docs_url=None if EM_PRODUCAO else "/api/docs",
    redoc_url=None if EM_PRODUCAO else "/api/redoc",
    openapi_url=None if EM_PRODUCAO else "/api/openapi.json",
)

app.state.limiter = limiter    
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENS_PERMITIDAS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(startup_router)
app.include_router(agents_router)
app.include_router(planning_item_router)
app.include_router(canvas_zone_router)
app.include_router(product_router)
app.include_router(simulation_interest_router)


@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verifica se a API está online e respondendo."""
    # TODO: Fazer uma verificação dos serviços essências estão funcionando, como o supabase.
    
    return {
        "status": "ok", 
        "ambiente": AMBIENTE
    }

