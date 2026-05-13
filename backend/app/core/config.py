from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "OCOP Traceability API"
    sqlserver_url: str = (
        "mssql+aioodbc://sa:YourStrong!Passw0rd@localhost:1433/ocop_traceability"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    mongodb_url: str = "mongodb://localhost:27017"
    redis_url: str = "redis://localhost:6379/0"
    mqtt_broker_url: str = "mqtt://localhost:1883"
    mqtt_topic: str = "ocop/sensors/#"
    blockchain_rpc_url: str = "http://127.0.0.1:7545"
    contract_address: str = ""
    private_key: str = ""
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
