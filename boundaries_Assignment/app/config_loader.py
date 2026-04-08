import json
from dataclasses import dataclass
from pathlib import Path


class ConfigurationError(Exception):
    """Raised when application configuration is missing or invalid."""


@dataclass(frozen=True)
class AppConfig:
    google_api_key: str


class ConfigLoader:
    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path

    def load(self) -> AppConfig:
        if not self._config_path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {self._config_path}. "
                "Create config.json from config.example.json."
            )

        try:
            raw_config = json.loads(self._config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ConfigurationError(
                f"Configuration file is not valid JSON: {self._config_path}"
            ) from exc

        api_key = str(raw_config.get("google_api_key", "")).strip()
        if not api_key:
            raise ConfigurationError(
                "Missing 'google_api_key' in configuration file."
            )

        return AppConfig(google_api_key=api_key)
