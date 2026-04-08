# Google Geocoding Console App

A cleanly structured console application that takes a location name and fetches latitude/longitude from the Google Geocoding API.

## Features

- Reads API key from configuration file (`config.json`)
- Validates user input
- Handles multiple geocoding results
- Handles API/network/configuration errors
- Prints structured JSON output

## Project Structure

- `main.py` - application entry point
- `app/config_loader.py` - configuration loading and validation
- `app/validators.py` - user input validation
- `app/geocoding_client.py` - Google Geocoding API integration
- `app/models.py` - domain models
- `app/output_formatter.py` - structured output formatting

## Setup

1. Copy `config.example.json` to `config.json`.
2. Add your API key in `config.json`:

```json
{
  "google_api_key": "YOUR_REAL_API_KEY"
}
```

3. Run the app:

```bash
python main.py
```

## Example Output

```json
{
  "query": "New York",
  "result_count": 2,
  "results": [
    {
      "formatted_address": "New York, NY, USA",
      "latitude": 40.7127753,
      "longitude": -74.0059728,
      "place_id": "ChIJOwg_06VPwokRYv534QaPC8g",
      "location_type": "APPROXIMATE"
    }
  ]
}
```
