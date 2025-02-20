import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Retrieve the NOAA API key from environment variables
NOAA_API_KEY = os.getenv("NOAA_API_KEY")

# Check if the key is fetched correctly
if NOAA_API_KEY is None:
    print("NOAA API key not found. Please check your environment variable.")
else:
    # Example URL for NOAA API endpoint with parameters
    url = f"https://api.weather.gov/alerts/active?area=CA"

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        
        # Define the path where you want to save the data inside your project directory
        file_path = "C:/Users/dhananjay vaidya/Downloads/DisasterProject/noaa_data.json"
        
        # Write the data to the file
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        
        print("Weather Data saved successfully to", file_path)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
