import json

from app.models import GeocodingResult


def format_geocoding_output(query: str, results: list[GeocodingResult]) -> str:
    output = {
        "query": query,
        "result_count": len(results),
        "results": [
            {
                "formatted_address": item.formatted_address,
                "latitude": item.coordinates.latitude,
                "longitude": item.coordinates.longitude,
                "place_id": item.place_id,
                "location_type": item.location_type,
            }
            for item in results
        ],
    }
    return json.dumps(output, indent=2)
