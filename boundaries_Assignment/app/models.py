from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class GeocodingResult:
    formatted_address: str
    coordinates: Coordinates
    place_id: str
    location_type: str
