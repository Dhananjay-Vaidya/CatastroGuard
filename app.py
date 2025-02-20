import streamlit as st
import json
from datetime import datetime
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

# Load NOAA Data
with open('processed_noaa_data.json', 'r') as file:
    noaa_data = json.load(file)

# Load Google News Data
with open('processed_google_news_data.json', 'r') as file:
    news_data = json.load(file)

# Function for Machine Learning Risk Prediction
def risk_prediction(description):
    train_data = [
        "Minor flooding expected in low-lying areas",
        "Severe hurricane approaching with high winds",
        "Moderate earthquake with potential damage",
        "High wind warning with power outages",
        "Flash flood alert with evacuation orders"
    ]
    train_labels = [1, 3, 2, 3, 3]  # 1=Low, 2=Moderate, 3=Severe
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(train_data)
    model = MultinomialNB()
    model.fit(X_train, train_labels)

    # Prediction
    X_test = vectorizer.transform([description])
    prediction = model.predict(X_test)
    return prediction[0]

# Function to Filter NOAA Data
def filter_noaa_data(location, event_type, severity_filter):
    filtered_data = []
    for item in noaa_data:
        if (location.lower() in item['area'].lower()) and (event_type.lower() in item['event'].lower()):
            # Apply severity filter if specified
            if severity_filter:
                if severity_filter.lower() in item['severity'].lower():
                    filtered_data.append(item)
            else:
                filtered_data.append(item)
    return filtered_data

# Function to Filter News Data
def filter_news_data(keyword):
    filtered_news = []
    for article in news_data:
        if keyword.lower() in article['headline'].lower() or keyword.lower() in article['description'].lower():
            filtered_news.append(article)
    return filtered_news

# Streamlit Interface
st.title('Disaster Response and Risk Prediction System')

# Sidebar for Disaster Type and Severity Filter
disaster_type = st.sidebar.selectbox(
    'Select Disaster Type',
    ['Flood', 'Earthquake', 'Wildfire', 'Hurricane']
)
severity_filter = st.sidebar.selectbox(
    'Filter by Severity',
    ['', 'Minor', 'Moderate', 'Severe']
)

# User Input for Location and Event Type
location_input = st.text_input('Enter Location (e.g., San Diego, CA)')
event_type_input = st.text_input('Enter Event Type (e.g., Flood, Wind, Storm)')

if st.button('Search Disaster Data'):
    if location_input and event_type_input:
        st.subheader('NOAA Disaster Alerts')
        noaa_results = filter_noaa_data(location_input, event_type_input, severity_filter)
        if noaa_results:
            for alert in noaa_results:
                st.markdown(f"### {alert['title']}")
                st.markdown(f"**Description:** {alert['description']}")
                st.markdown(f"**Severity:** {alert['severity']}")
                st.markdown(f"**Area:** {alert['area']}")
                st.markdown(f"**Event Type:** {alert['event']}")
                st.markdown(f"**Start:** {alert['start']}")
                st.markdown(f"**End:** {alert['end']}")

                # ML Risk Prediction
                predicted_risk = risk_prediction(alert['description'])
                risk_level = {1: 'Low', 2: 'Moderate', 3: 'Severe'}
                st.markdown(f"**Predicted Risk Level:** {risk_level[predicted_risk]}")
                
                # Real-Time Notification for High Risk
                if predicted_risk == 3:
                    st.error(f"⚠️ Critical Alert: {alert['title']} in {alert['area']}")
                elif predicted_risk == 2:
                    st.warning(f"⚠️ Moderate Alert: {alert['title']} in {alert['area']}")
                else:
                    st.success(f"✅ Low Risk: {alert['title']} in {alert['area']}")
                
                st.markdown("---")
        else:
            st.write("No NOAA alerts found for the given location and event type.")
    else:
        st.write("Please enter both location and event type.")

# User Input for News Search
keyword_input = st.text_input('Enter Keyword for News Search')

if st.button('Search News'):
    if keyword_input:
        st.subheader('Relevant News Articles')
        news_results = filter_news_data(keyword_input)
        if news_results:
            for news in news_results:
                st.markdown(f"### {news['headline']}")
                st.markdown(f"**Source:** {news['source']}")
                st.markdown(f"**Published At:** {news['publishedAt']}")
                st.markdown(f"**Description:** {news['description']}")
                st.markdown(f"[Read More]({news['url']})")
                st.markdown("---")
        else:
            st.write("No news articles found for the given keyword.")
    else:
        st.write("Please enter a keyword to search news.")

# Footer Section
st.markdown("""
    ---
    Built with Streamlit, TextBlob, and Scikit-learn.
    """)
