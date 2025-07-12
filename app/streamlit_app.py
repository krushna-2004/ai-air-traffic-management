import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'utils')))
from geo_utils import predict_position, is_conflict

# Load model and features
model, model_features = joblib.load("D:/ai-air-traffic-management\models\delay_model.pkl")

st.title("✈️ Flight Delay Predictor")
st.markdown("Predict if a flight will be delayed based on schedule and route details.")

# --- User Inputs ---
st.sidebar.header("📋 Enter Flight Details")

month = st.sidebar.selectbox("Month", list(range(1, 13)))
day = st.sidebar.slider("Day of Month", 1, 31)
day_of_week = st.sidebar.selectbox("Day of Week (1=Mon)", list(range(1, 8)))

crs_dep_time = st.sidebar.number_input("Scheduled Departure Time (HHMM)", 0, 2359, step=1)

carrier = st.sidebar.selectbox("Airline Carrier", [
    'AA', 'DL', 'UA', 'WN', 'B6', 'AS', 'F9', 'NK', 'OO', 'VX'  # Add more based on your dataset
])

origin = st.sidebar.text_input("Origin Airport Code (e.g. ATL, JFK)", "ATL")
dest = st.sidebar.text_input("Destination Airport Code (e.g. LAX, ORD)", "LAX")

# --- Create input DataFrame ---
input_data = pd.DataFrame([{
    "Month": month,
    "DayofMonth": day,
    "DayOfWeek": day_of_week,
    "CRSDepTime": crs_dep_time,
    "UniqueCarrier": carrier,
    "Origin": origin,
    "Dest": dest
}])

# One-hot encode input to match model training
input_encoded = pd.get_dummies(input_data)

# Align with training features (fill missing columns)
input_encoded = input_encoded.reindex(columns=model_features, fill_value=0)

# --- Prediction ---
if st.button("✈️ Predict Delay"):
    prediction = model.predict(input_encoded)[0]
    proba = model.predict_proba(input_encoded)[0][1]

    if prediction == 1:
        st.error(f"⚠️ This flight is likely to be **Delayed**. Probability: {proba:.2f}")
    else:
        st.success(f"✅ This flight is likely to be **On Time**. Probability: {1 - proba:.2f}")



# st.set_page_config(page_title="Flight Conflict Checker", layout="centered")

# st.title("🛫 Flight Conflict Predictor")

st.markdown("Enter a new flight's details. The system will predict if it conflicts with any aircraft in the airspace 10 minutes from now.")

# Load existing flights from data file
existing_df = pd.read_csv("D:/ai-air-traffic-management\data\simulated_aircraft_positions.csv")

# ✈️ Input for new flight
with st.form("flight_form"):
    callsign = st.text_input("Callsign", "TEST123")
    lat = st.number_input("Latitude", value=28.6)
    lon = st.number_input("Longitude", value=77.2)
    alt = st.number_input("Altitude (meters)", value=10000)
    velocity = st.number_input("Velocity (m/s)", value=230)
    heading = st.number_input("Heading (0-360°)", value=90)
    submitted = st.form_submit_button("Check for Conflict")

if submitted:
    # Store input in session_state
    st.session_state["new_flight_input"] = {
        'callsign': callsign,
        'lat': lat,
        'lon': lon,
        'alt': alt,
        'velocity': velocity,
        'heading': heading
    }

# Run only if user submitted or session has data
if "new_flight_input" in st.session_state:
    user_input = st.session_state["new_flight_input"]
    new_lat, new_lon = predict_position(user_input['lat'], user_input['lon'], user_input['velocity'], user_input['heading'], 10)
    
    new_flight = {
        'icao24': 'manual',
        'callsign': user_input['callsign'],
        'lat': new_lat,
        'lon': new_lon,
        'alt': user_input['alt']
    }

    # Predict existing aircraft future positions
    future_existing = []
    for i, row in existing_df.iterrows():
        f_lat, f_lon = predict_position(row['latitude'], row['longitude'], row['velocity'], row['heading'], 10)
        future_existing.append({
            'icao24': row['icao24'],
            'callsign': row['callsign'],
            'lat': f_lat,
            'lon': f_lon,
            'alt': row['baro_altitude']
        })

    # Map and Conflict Detection
    conflict_list = []
    m = folium.Map(location=[new_lat, new_lon], zoom_start=5)

    folium.Marker(
        location=[new_lat, new_lon],
        popup=f"{user_input['callsign']} (new)",
        icon=folium.Icon(color='green')
    ).add_to(m)

    for other in future_existing:
        folium.Marker(
            location=[other['lat'], other['lon']],
            popup=f"{other['callsign']}",
            icon=folium.Icon(color='blue')
        ).add_to(m)

        if is_conflict(new_flight, other):
            conflict_list.append(other['callsign'])
            folium.PolyLine(
                locations=[[new_lat, new_lon], [other['lat'], other['lon']]],
                color='red',
                tooltip=f"Conflict: {user_input['callsign']} ↔ {other['callsign']}"
            ).add_to(m)

    st.subheader("🗺️ Predicted Conflict Map")
    st_data = st_folium(m, width=800, height=600)

    if conflict_list:
        st.error(f"⚠️ Conflict Detected with: {', '.join(conflict_list)}")
    else:
        st.success("✅ No Conflict Detected for the Entered Flight.")
