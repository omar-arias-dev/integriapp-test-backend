from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.configuration.configuration import settings
from app.core.dabatase import engine, Base
from app.controller import VehicleController, RouteController, PerformanceController


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="API REST con FastAPI y PostgreSQL",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(VehicleController.router)
app.include_router(RouteController.router)
app.include_router(PerformanceController.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )