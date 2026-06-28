import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.presentation.middlewares.logging_middleware import LoggingMiddleware

from app.core.config import settings
from app.infrastructure.database.sqlserver.session import init_db
from app.infrastructure.mqtt.hive_mqtt_client import HiveMqttClient
from app.infrastructure.mqtt.mqtt_message_adapter import MqttMessageAdapter
from app.infrastructure.mqtt.mqtt_subscriber import MqttSubscriber
from app.infrastructure.queue.redis_client import get_redis_client
from app.infrastructure.queue.redis_queue_adapter import RedisQueueAdapter
from app.presentation.api.v1.auth_controller import router as auth_router
from app.presentation.api.v1.batch_controller import router as batch_router
from app.presentation.api.v1.container_controller import router as container_router
from app.presentation.api.v1.crop_type_controller import router as crop_type_router
from app.presentation.api.v1.farm_controller import router as farm_router
from app.presentation.api.v1.risk_rule_controller import router as risk_rule_router
from app.presentation.api.v1.shipment_controller import router as shipment_router
from app.presentation.api.v1.sensor_controller import router as sensor_router
from app.presentation.api.v1.traceability_controller import router as traceability_router
from app.presentation.api.v1.user_controller import router as user_router
from app.presentation.api.v1.blockchain_controller import router as blockchain_router
from app.presentation.api.v1.dashboard_controller import router as dashboard_router
from app.presentation.api.v1.chemical_controller import router as chemical_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="OCOP Traceability API",
        description="API quản lý truy xuất nguồn gốc sản phẩm OCOP — IoT + Blockchain",
        version="1.0.0",
    )
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:4200",
            "http://127.0.0.1:4200",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup() -> None:
        try:
            await init_db()
            
            # Seed default admin account
            from app.infrastructure.database.sqlserver.session import async_session
            from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
            from app.application.services.auth_service import AuthService
            from app.application.dto.auth_dto import RegisterRequest
            from app.infrastructure.database.seed_data import seed_all
            
            async with async_session() as session:
                user_repo = SqlUserRepository(session)
                existing = await user_repo.find_by_email("admin@ocop.vn")
                if not existing:
                    auth_service = AuthService(user_repo)
                    await auth_service.register(RegisterRequest(
                        full_name="Admin",
                        email="admin@ocop.vn",
                        password="Abc@1234",
                        role=0
                    ))
                    logger.info("Created default admin account: admin@ocop.vn")

            # Seed dữ liệu mẫu (bỏ qua nếu đã có)
            async with async_session() as session:
                await seed_all(session)
        except Exception as error:
            logger.warning("Database initialization skipped: %s", error)

        try:
            mqtt_client = HiveMqttClient(settings.mqtt_broker_url)
            mqtt_subscriber = MqttSubscriber(
                mqtt_client=mqtt_client,
                message_adapter=MqttMessageAdapter(),
                queue_client=RedisQueueAdapter(get_redis_client()),
                topic=settings.mqtt_topic,
            )
            await mqtt_subscriber.start()
            print(f"[Startup] MQTT subscriber started. Broker={settings.mqtt_broker_url}, Topic={settings.mqtt_topic}")
            logger.info("MQTT subscriber started on topic %s", settings.mqtt_topic)
        except Exception as error:
            print(f"[Startup] MQTT subscriber FAILED: {error}")
            logger.warning("MQTT subscriber failed to start: %s", error)

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
    app.include_router(user_router)
    app.include_router(blockchain_router)
    app.include_router(dashboard_router)
    app.include_router(chemical_router)
    return app
