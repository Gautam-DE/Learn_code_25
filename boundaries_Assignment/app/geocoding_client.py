import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import urlopen

from app.models import Coordinates, GeocodingResult


class GeocodingError(Exception):
    """Raised when the geocoding API call fails."""


class GoogleGeocodingClient:
    BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def geocode(self, location: str) -> list[GeocodingResult]:
        encoded_location = quote_plus(location)
        url = f"{self.BASE_URL}?address={encoded_location}&key={self._api_key}"

        try:
            with urlopen(url, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise GeocodingError(f"HTTP error from geocoding service: {exc.code}") from exc
        except URLError as exc:
            raise GeocodingError(f"Network error while contacting geocoding service: {exc.reason}") from exc
        except TimeoutError as exc:
            raise GeocodingError("Request to geocoding service timed out.") from exc
        except json.JSONDecodeError as exc:
            raise GeocodingError("Invalid response format from geocoding service.") from exc

        status = payload.get("status", "UNKNOWN")
        if status == "ZERO_RESULTS":
            return []
        if status != "OK":
            error_message = payload.get("error_message", "No additional details provided.")
            raise GeocodingError(f"Geocoding API returned {status}: {error_message}")

        results = payload.get("results", [])
        return [self._map_result(item) for item in results]

    @staticmethod
    def _map_result(item: dict) -> GeocodingResult:
        geometry = item.get("geometry", {})
        location = geometry.get("location", {})

        return GeocodingResult(
            formatted_address=item.get("formatted_address", "Unknown"),
            coordinates=Coordinates(
                latitude=float(location.get("lat", 0.0)),
                longitude=float(location.get("lng", 0.0)),
            ),
            place_id=item.get("place_id", "Unknown"),
            location_type=geometry.get("location_type", "Unknown"),
        )
