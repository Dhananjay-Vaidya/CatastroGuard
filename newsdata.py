import requests
import json
import os

# Get the Google News data (assuming you already have the API call here)
api_key = os.getenv("GOOGLE_NEWS_API_KEY")
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Define the path where you want to save the data inside your project directory
    file_path = "C:/Users/dhananjay vaidya/Downloads/DisasterProject/google_news_data.json"
    
    # Write the data to the file
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Data saved successfully to {file_path}")
else:
    print(f"Failed to retrieve data: {response.status_code}")
