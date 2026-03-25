"""
Currency Converter Application
This script converts currency amounts using real-time exchange rates from open.er-api.com
"""

# Import libraries for HTTP requests and JSON parsing
import requests
import json

# Display welcome message to user
print("Welcome to the Currency Converter!")
print("")

# Collect user inputs for conversion
amount = float(input("Enter the amount you want to convert: "))
from_cur = input("Enter the currency you have (e.g. USD): ").upper()
to_cur = input("Enter the currency you want (e.g. AED): ").upper()

print("")
print("Getting the exchange rate...")

# Construct API URL to fetch exchange rates for the base currency
# Using open.er-api.com API endpoint (free, no authentication required)
url = f"https://open.er-api.com/v6/latest?base={from_cur}"

# Wrap API call in try-except to handle network and timeout errors
try:
    # Make GET request with 5-second timeout to prevent hanging
    response = requests.get(url, timeout=5)
    
    # Check if the HTTP response was successful (status code 200)
    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        print("Please check your internet connection or try again later.")
    else:
        # Parse JSON response from API
        try:
            data = response.json()
            
            # Validate that the API response contains exchange rates
            if "rates" not in data:
                print(f"Error: Invalid response from API")
                print(f"Response: {data}")
            # Check if the target currency exists in the available rates
            elif to_cur not in data["rates"]:
                print(f"Error: Currency '{to_cur}' not found.")
                print(f"Available currencies: {', '.join(list(data['rates'].keys())[:10])}...")
            else:
                # Extract exchange rate and calculate conversion
                rate = data["rates"][to_cur]
                result = amount * rate
                result = round(result, 2)

                # Display conversion result to user
                print("")
                print("Done! Here is the result:")
                print(str(amount) + " " + from_cur + " = " + str(result) + " " + to_cur)
                print("(Exchange rate: 1 " + from_cur + " = " + str(rate) + " " + to_cur + ")")
        # Handle JSON parsing errors if API response is invalid
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Error parsing API response: {e}")
            print(f"Response: {response.text[:200]}")
# Handle network timeout errors (request takes too long)
except requests.exceptions.Timeout:
    print("Error: Request timed out. Please check your internet connection.")
# Handle all other network and connection errors
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to connect to API: {e}")