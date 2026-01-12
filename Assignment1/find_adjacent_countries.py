import json
import os


def load_country_data():
    """Load country data from JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "countries_data.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find countries_data.json in {script_dir}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in countries_data.json")
        return {}


def get_adjacent_countries(country_code, country_data):
    """Get adjacent countries for a given country code."""
    country_code_upper = country_code.upper()
    
    if country_code_upper not in country_data:
        return None, None
    
    country_info = country_data[country_code_upper]
    country_name = country_info["name"]
    adjacent_countries = country_info["adjacent"]
    
    return country_name, adjacent_countries


def main():
    """Main function to run the adjacent countries finder."""
    print("Adjacent Countries Finder")
    
    # Load country data from JSON file
    country_data = load_country_data()
    
    if not country_data:
        print("Failed to load country data. Exiting.")
        return
    
    while True:
        country_code = input("\nEnter a Country Code (e.g., IN/US/NZ) or 'Q' to quit: ").strip()
        
        if country_code.upper() == 'Q':
            print("Thank you for using Adjacent Countries Finder!")
            break
        
        if not country_code:
            print("Please enter a valid country code.")
            continue
        
        country_name, adjacent_countries = get_adjacent_countries(country_code, country_data)
        
        if country_name is None:
            print(f"Country code '{country_code}' not found in the database.")
            print("Available country codes:", ", ".join(country_data.keys()))
        else:
            print(f"\nCountry: {country_name}")
            print(f"Adjacent Countries ({len(adjacent_countries)}):")
            for i, adj_country in enumerate(adjacent_countries, 1):
                print(f"  {i}. {adj_country}")


if __name__ == "__main__":
    main()

