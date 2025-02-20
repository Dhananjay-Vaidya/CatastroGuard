# Disaster Response and Risk Prediction System

This project is a **Disaster Response and Risk Prediction System** that utilizes NOAA data and Google News articles to provide real-time alerts and insights about natural disasters, such as floods, earthquakes, wildfires, and hurricanes. The system is designed to assist in disaster management and resource allocation by displaying relevant disaster alerts and news articles through an interactive Streamlit dashboard.

---

## 🚀 Features
- 🔥 **Real-time NOAA Alerts**: Fetches active disaster alerts from NOAA.
- 📰 **Google News Integration**: Retrieves disaster-related news headlines.
- 📊 **Machine Learning-based Risk Prediction**: Uses **Naive Bayes Classification** to predict disaster severity.
- 📍 **Location-based Filtering**: Search alerts by **region, severity, and disaster type**.
- 🔔 **Real-time Notifications**: Highlights **critical alerts** for immediate attention.
- 🎨 **Streamlit Web App**: Provides an interactive dashboard.

---

## Tech Stack & Tools
- **Programming Language**: Python
- **Web Framework**: Streamlit
- **Data Sources**:
  - NOAA API (Processed Alerts Data)
  - Google News API (Processed News Articles)
- **JSON Processing**: Using Python's `json` module
- **Date Handling**: Using `datetime` module in Python

---

## Data Sources
1. **NOAA Alerts Data**: Processed NOAA alerts related to floods, wildfires, earthquakes, and more.
2. **Google News Data**: Processed news articles about natural disasters from reliable news sources.

---

## Installation

### Prerequisites
- Python 3.x installed on your system.
- Streamlit library for running the web application.

### Clone the Repository
```bash
git clone 
cd disaster-response-system
