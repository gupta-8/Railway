from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    fare_per_km: int = 2

settings = Settings()
