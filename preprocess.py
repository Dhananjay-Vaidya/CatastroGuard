import json
import os

# Define paths for the raw and preprocessed data files
noaa_raw_path = "C:/Users/dhananjay vaidya/Downloads/DisasterProject/noaa_data.json"
news_raw_path = "C:/Users/dhananjay vaidya/Downloads/DisasterProject/google_news_data.json"
noaa_processed_path = "C:/Users/dhananjay vaidya/Downloads/DisasterProject/processed_noaa_data.json"
news_processed_path = "C:/Users/dhananjay vaidya/Downloads/DisasterProject/processed_google_news_data.json"

# 1. **Loading NOAA Data**
with open(noaa_raw_path, "r") as file:
    noaa_data = json.load(file)

# 2. **Preprocessing NOAA Data**
# Extract the relevant details from the NOAA data (alerts)
cleaned_noaa_data = []
if "features" in noaa_data:
    for alert in noaa_data["features"]:
        cleaned_alert = {
            "title": alert.get("properties", {}).get("headline", ""),
            "description": alert.get("properties", {}).get("description", ""),
            "severity": alert.get("properties", {}).get("severity", ""),
            "area": alert.get("properties", {}).get("areaDesc", ""),
            "event": alert.get("properties", {}).get("event", ""),
            "start": alert.get("properties", {}).get("effective", ""),
            "end": alert.get("properties", {}).get("expires", ""),
        }
        cleaned_noaa_data.append(cleaned_alert)

# Save the processed NOAA data to a new JSON file
with open(noaa_processed_path, "w") as processed_file:
    json.dump(cleaned_noaa_data, processed_file, indent=4)

# 3. **Loading Google News Data**
with open(news_raw_path, "r") as file:
    news_data = json.load(file)

# 4. **Preprocessing Google News Data**
# Extract the relevant details from the Google News data (articles)
cleaned_news_data = []
if "articles" in news_data:
    for article in news_data["articles"]:
        cleaned_article = {
            "headline": article.get("title", ""),
            "description": article.get("description", ""),
            "source": article.get("source", {}).get("name", ""),
            "publishedAt": article.get("publishedAt", ""),
            "url": article.get("url", ""),
            "content": article.get("content", ""),
        }
        cleaned_news_data.append(cleaned_article)

# Save the processed Google News data to a new JSON file
with open(news_processed_path, "w") as processed_file:
    json.dump(cleaned_news_data, processed_file, indent=4)

# Confirm that preprocessing was successful
print(f"Preprocessing complete! Processed NOAA data saved to: {noaa_processed_path}")
print(f"Preprocessed Google News data saved to: {news_processed_path}")
