COUNTRY_DATA = {
    "IN": {
        "name": "India",
        "adjacent": ["Pakistan", "China", "Nepal", "Bhutan", "Bangladesh", "Myanmar", "Sri Lanka"]
    },
    "US": {
        "name": "United States",
        "adjacent": ["Canada", "Mexico"]
    },
    "NZ": {
        "name": "New Zealand",
        "adjacent": ["Australia"]
    },
    "CA": {
        "name": "Canada",
        "adjacent": ["United States"]
    },
    "MX": {
        "name": "Mexico",
        "adjacent": ["United States", "Guatemala", "Belize"]
    },
    "CN": {
        "name": "China",
        "adjacent": ["India", "Russia", "Mongolia", "North Korea", "Vietnam", "Myanmar", "Nepal"]
    },
    "PK": {
        "name": "Pakistan",
        "adjacent": ["India", "Afghanistan", "Iran", "China"]
    },
    "AU": {
        "name": "Australia",
        "adjacent": ["New Zealand", "Indonesia", "Papua New Guinea"]
    },
    "GB": {
        "name": "United Kingdom",
        "adjacent": ["Ireland", "France"]
    },
    "FR": {
        "name": "France",
        "adjacent": ["United Kingdom", "Germany", "Spain", "Italy", "Belgium", "Switzerland"]
    },
    "DE": {
        "name": "Germany",
        "adjacent": ["France", "Poland", "Austria", "Switzerland", "Netherlands", "Belgium"]
    },
    "JP": {
        "name": "Japan",
        "adjacent": ["South Korea", "China", "Russia"]
    },
    "BR": {
        "name": "Brazil",
        "adjacent": ["Argentina", "Peru", "Colombia", "Venezuela", "Bolivia", "Paraguay", "Uruguay"]
    },
    "RU": {
        "name": "Russia",
        "adjacent": ["China", "Mongolia", "Kazakhstan", "Ukraine", "Finland", "Norway", "Japan"]
    },
    "EG": {
        "name": "Egypt",
        "adjacent": ["Libya", "Sudan", "Israel", "Palestine"]
    }
}


def get_adjacent_countries(country_code):
    country_code_upper = country_code.upper()
    
    if country_code_upper not in COUNTRY_DATA:
        return None, None
    
    country_info = COUNTRY_DATA[country_code_upper]
    country_name = country_info["name"]
    adjacent_countries = country_info["adjacent"]
    
    return country_name, adjacent_countries


def main():
    print("Adjacent Countries Finder")
    
    while True:
        country_code = input("\nEnter a Country Code (e.g., IN/US/NZ) or 'Q' to quit: ").strip()
        
        if country_code.upper() == 'Q':
            print("Thank you for using Adjacent Countries Finder!")
            break
        
        if not country_code:
            print("Please enter a valid country code.")
            continue
        
        country_name, adjacent_countries = get_adjacent_countries(country_code)
        
        if country_name is None:
            print(f"Country code '{country_code}' not found in the database.")
            print("Available country codes:", ", ".join(COUNTRY_DATA.keys()))
        else:
            print(f"\nCountry: {country_name}")
            print(f"Adjacent Countries ({len(adjacent_countries)}):")
            for i, adj_country in enumerate(adjacent_countries, 1):
                print(f"  {i}. {adj_country}")


if __name__ == "__main__":
    main()

