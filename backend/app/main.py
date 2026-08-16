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


from app.core.limiter import limiter

app = FastAPI(
    title="Plataforma Core API",
    description="API principal responsável pelo gerenciamento e materialização de dados do produto.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.state.limiter = limiter    
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

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
app.include_router(startup_router)
app.include_router(agents_router)
app.include_router(planning_item_router)
app.include_router(canvas_zone_router)
app.include_router(product_router)


@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verifica se a API está online e respondendo."""
    return {"status": "ok", "ambiente": "desenvolvimento"}

