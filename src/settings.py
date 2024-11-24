from dataclasses import dataclass
from os import environ


@dataclass
class Settings:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    KAFKA_HOST: str
    KAFKA_PORT: int
    KAFKA_TOPIC: str
    KAFKA_CONSUMER_GROUP: str


settings = Settings(
    POSTGRES_USER=environ["POSTGRES_USER"],
    POSTGRES_PASSWORD=environ["POSTGRES_PASSWORD"],
    POSTGRES_HOST=environ["POSTGRES_HOST"],
    POSTGRES_PORT=int(environ["POSTGRES_PORT"]),
    POSTGRES_DB=environ["POSTGRES_DB"],
    KAFKA_HOST=environ.get("KAFKA_HOST", "127.0.0.1"),
    KAFKA_PORT=int(environ.get("KAFKA_PORT", 9092)),
    KAFKA_TOPIC=environ.get("KAFKA_TOPIC", "smit-logger"),
    KAFKA_CONSUMER_GROUP=environ.get("KAFKA_CONSUMER_GROUP", "group-id"),
)
