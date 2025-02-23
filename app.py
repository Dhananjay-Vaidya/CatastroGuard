import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from streamlit_folium import st_folium
import folium
import altair as alt

# Page Configuration
st.set_page_config(
    page_title="Disaster Response System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .stSelectbox { margin-bottom: 1rem; }
    .risk-badge { padding: 0.5rem; border-radius: 5px; font-weight: bold; }
    .sidebar .sidebar-content { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    noaa_file = os.path.join("data", "processed_noaa_data.json")
    news_file = os.path.join("data", "processed_google_news_data.json")

    if not os.path.exists(noaa_file) or not os.path.exists(news_file):
        st.error("Error: Data files not found. Ensure they are inside the 'data/' folder.")
        return [], []

    with open(noaa_file, 'r') as file:
        noaa_data = json.load(file)

    with open(news_file, 'r') as file:
        news_data = json.load(file)

    return noaa_data, news_data

noaa_data, news_data = load_data()

# Enhanced Risk Prediction
def enhanced_risk_prediction(description):
    train_data = [
        "Minor flooding expected in low-lying areas",
        "Severe hurricane approaching with high winds",
        "Moderate earthquake with potential damage",
        "High wind warning with power outages",
        "Flash flood alert with evacuation orders",
        "Tropical storm warning issued",
        "Category 5 hurricane expected",
        "Tsunami warning for coastal areas",
        "Volcanic eruption imminent",
        "Extreme heat advisory issued"
    ]
    train_labels = [1, 3, 2, 3, 3, 2, 3, 3, 3, 2]  # 1=Low, 2=Moderate, 3=Severe

    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(train_data)
    model = MultinomialNB()
    model.fit(X_train, train_labels)

    X_test = vectorizer.transform([description])
    prediction = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[0]
    return prediction[0], probabilities

# Sidebar Navigation
st.sidebar.image("https://via.placeholder.com/150x150.png?text=DRS", width=150)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Search Alerts", "News Feed", "Analytics"])

# Filters Section in Sidebar
st.sidebar.title("Filters")
disaster_type = st.sidebar.selectbox('Disaster Type', ['All', 'Flood', 'Earthquake', 'Wildfire', 'Hurricane', 'Tornado', 'Tsunami'])
severity_filter = st.sidebar.selectbox('Severity Level', ['All', 'Minor', 'Moderate', 'Severe'])
date_range = st.sidebar.date_input("Date Range", value=(datetime.now().date(), datetime.now().date()))

# Dashboard
if page == "Dashboard":
    st.title("🚨 Disaster Response Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Alerts", len(noaa_data))
    with col2:
        st.metric("High Risk Areas", sum(1 for item in noaa_data if item.get('severity') == 'Severe'))
    with col3:
        st.metric("Affected Regions", len(set(item.get('area', 'Unknown') for item in noaa_data)))
    with col4:
        st.metric("News Coverage", len(news_data))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Geographic Distribution of Alerts")
        m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
        st_folium(m, width=700, height=500)

    with col2:
        st.subheader("Alerts by Type")
        event_list = [item.get('event', 'Unknown') for item in noaa_data if 'event' in item]
        df = pd.DataFrame(event_list, columns=['Event'])
        df = df.groupby('Event').size().reset_index(name='Count')

        if not df.empty:
            fig = px.pie(df, values='Count', names='Event', hole=0.3)
            st.plotly_chart(fig)

# Search Alerts
elif page == "Search Alerts":
    st.title("🔍 Search Alerts")

    location_input = st.text_input('Location', placeholder='e.g., California')
    event_type_input = st.selectbox('Event Type', ['All'] + list(set(item.get('event', 'Unknown') for item in noaa_data)))
    severity_filter = st.selectbox('Severity', ['All', 'Minor', 'Moderate', 'Severe'])

    filtered_alerts = [
        alert for alert in noaa_data
        if (location_input.lower() in alert.get('area', '').lower() if location_input else True) and
        (event_type_input == 'All' or alert.get('event') == event_type_input) and
        (severity_filter == 'All' or alert.get('severity') == severity_filter)
    ]

    if not filtered_alerts:
        st.warning("No alerts found for the selected filters.")

    for alert in filtered_alerts:
        with st.expander(f"🚨 {alert.get('title', 'Unknown Title')}"):
            st.markdown(f"**Event Type:** {alert.get('event', 'Unknown')}")
            st.markdown(f"**Area:** {alert.get('area', 'Unknown')}")
            st.markdown(f"**Severity:** {alert.get('severity', 'Unknown')}")
            st.markdown(f"**Start Time:** {alert.get('start', 'N/A')}")
            st.markdown(f"**End Time:** {alert.get('end', 'N/A')}")

# News Feed
elif page == "News Feed":
    st.title("📰 News Feed")
    keyword_input = st.text_input('Search News', placeholder='Enter keywords...')
    filtered_news = [news for news in news_data if keyword_input.lower() in news.get('headline', '').lower()] if keyword_input else news_data

    if not filtered_news:
        st.warning("No news articles found.")

    for news in filtered_news:
        with st.expander(f"📰 {news.get('headline', 'Unknown Title')}"):
            st.markdown(f"**Source:** {news.get('source', 'Unknown')}")
            st.markdown(f"**Published:** {news.get('publishedAt', 'N/A')}")
            st.markdown(f"**Description:** {news.get('description', 'No description available')}")

elif page == "Analytics":
    st.title("📊 Disaster Analytics")

    # Ensure we have data before proceeding
    if not noaa_data:
        st.warning("No alert data available for analytics.")
    else:
        df_alerts = pd.DataFrame(noaa_data)

        # Convert 'start' and 'end' to datetime safely
        df_alerts['start'] = pd.to_datetime(df_alerts['start'], errors='coerce')
        df_alerts['end'] = pd.to_datetime(df_alerts['end'], errors='coerce')

        # Remove any null dates
        df_alerts = df_alerts.dropna(subset=['start', 'end'])

        st.subheader("📈 Alert Trends Over Time")
        if not df_alerts.empty:
            chart = alt.Chart(df_alerts).mark_line().encode(
                x='start:T',
                y='count():Q',
                color='event:N'
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No data available for time series analysis.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔥 Event Type Distribution")
            df_event_counts = df_alerts.groupby('event').size().reset_index(name='Count')

            if not df_event_counts.empty:
                fig = px.bar(df_event_counts, x='event', y='Count',
                             labels={'x': 'Event Type', 'y': 'Count'}, 
                             title="Alerts by Event Type")
                st.plotly_chart(fig)
            else:
                st.warning("No data available for event type distribution.")

        with col2:
            st.subheader("📍 Affected Regions Distribution")
            df_area_counts = df_alerts.groupby('area').size().reset_index(name='Count')

            if not df_area_counts.empty:
                fig = px.bar(df_area_counts, x='area', y='Count',
                             labels={'x': 'Area', 'y': 'Count'},
                             title="Alerts by Affected Regions")
                st.plotly_chart(fig)
            else:
                st.warning("No data available for affected regions.")

        st.subheader("📅 Alert Timeline")
        if not df_alerts.empty:
            timeline_chart = alt.Chart(df_alerts).mark_rect().encode(
                x='start:T',
                x2='end:T',
                y='event:N',
                color='severity:N',
                tooltip=['title', 'area', 'severity', 'start', 'end']
            ).properties(height=300)
            st.altair_chart(timeline_chart, use_container_width=True)
        else:
            st.warning("No data available for timeline analysis.")

# Footer
st.markdown("""
    ---
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit, Plotly, and Machine Learning</p>
        <p>© 2025 Disaster Response System</p>
    </div>
    """, unsafe_allow_html=True)
