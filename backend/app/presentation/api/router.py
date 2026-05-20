from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.infrastructure.database.sqlserver.session import init_db
from app.presentation.api.v1.auth_controller import router as auth_router
from app.presentation.api.v1.batch_controller import router as batch_router
from app.presentation.api.v1.container_controller import router as container_router
from app.presentation.api.v1.crop_type_controller import router as crop_type_router
from app.presentation.api.v1.farm_controller import router as farm_router
from app.presentation.api.v1.risk_rule_controller import router as risk_rule_router
from app.presentation.api.v1.shipment_controller import router as shipment_router
from app.presentation.api.v1.sensor_controller import router as sensor_router
from app.presentation.api.v1.traceability_controller import router as traceability_router


def create_app() -> FastAPI:
    app = FastAPI(title="OCOP Traceability API")

    @app.on_event("startup")
    async def startup() -> None:
        await init_db()

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, error: ValueError):
        detail = str(error)
        status_code = 404 if "not found" in detail.lower() else 400
        return JSONResponse(status_code=status_code, content={"detail": detail})

    app.include_router(auth_router)
    app.include_router(batch_router)
    app.include_router(container_router)
    app.include_router(crop_type_router)
    app.include_router(farm_router)
    app.include_router(risk_rule_router)
    app.include_router(shipment_router)
    app.include_router(sensor_router)
    app.include_router(traceability_router)
    return app
