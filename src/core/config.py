import os

class Settings:
    WRITER_DATABASE_URL: str = os.getenv(
        "WRITER_DATABASE_URL", 
        "postgresql+psycopg2://postgres:postgres@pg_primary:5432/mydatabase"
    )
    READER_DATABASE_URL: str = os.getenv(
        "READER_DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@pg_replica:5432/mydatabase"
    )

    # RabbitMQ
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super_secret_key")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

settings = Settings()
