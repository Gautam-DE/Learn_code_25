from pathlib import Path

from app.config_loader import ConfigLoader, ConfigurationError
from app.geocoding_client import GeocodingError, GoogleGeocodingClient
from app.output_formatter import format_geocoding_output
from app.validators import ValidationError, validate_location_input


def run() -> None:
    config_path = Path(__file__).with_name("config.json")

    try:
        config = ConfigLoader(config_path).load()
    except ConfigurationError as exc:
        print(f"Configuration error: {exc}")
        return

    location = input("Enter a location: ")

    try:
        validated_location = validate_location_input(location)
    except ValidationError as exc:
        print(f"Input error: {exc}")
        return

    client = GoogleGeocodingClient(config.google_api_key)

    try:
        results = client.geocode(validated_location)
    except GeocodingError as exc:
        print(f"Service error: {exc}")
        return

    if not results:
        print("No results found for the provided location.")
        return

    print(format_geocoding_output(validated_location, results))


if __name__ == "__main__":
    run()
