import requests
import csv

def fetch_and_format_to_csv(api_key):
    # API endpoint
    api_url = f"https://airlabs.co/api/v9/flights?api_key={api_key}"

    try:
        # Fetch data from the API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        # Parse JSON response
        data = response.json()
        print(data)

        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")

# Replace 'your_api_key' with your actual API key
api_key = 'ec3717ce-36bf-46b8-b8fe-356638bd8236'
fetch_and_format_to_csv(api_key)
