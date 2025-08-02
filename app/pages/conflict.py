import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from utils.geo_utils import predict_position, is_conflict

st.markdown("<h1 style='font-size: 25px;'>🛫 Flight Conflict Checker</h1>", unsafe_allow_html=True)
st.markdown("Enter a new flight's details. The system will check for any conflicts in the airspace 10 minutes from now.")

existing_df = pd.read_csv("D:/ai-air-traffic-management/data/simulated_aircraft_positions.csv")

# 🔄 Two columns: left for input, right for result
left_col, right_col = st.columns(2)

# ✈️ User input in left column
with left_col:
    with st.form("flight_form"):
        callsign = st.text_input("Callsign", "TEST123")
        lat = st.number_input("Latitude", value=28.6)
        lon = st.number_input("Longitude", value=77.2)
        alt = st.number_input("Altitude (meters)", value=10000)
        velocity = st.number_input("Velocity (m/s)", value=230)
        heading = st.number_input("Heading (0-360°)", value=90)
        submitted = st.form_submit_button("Check for Conflict")

    if submitted:
        st.session_state["new_flight_input"] = {
            'callsign': callsign,
            'lat': lat,
            'lon': lon,
            'alt': alt,
            'velocity': velocity,
            'heading': heading
        }

# ✅ Conflict result in right column
if "new_flight_input" in st.session_state:
    user_input = st.session_state["new_flight_input"]

    new_lat, new_lon = predict_position(
        user_input['lat'],
        user_input['lon'],
        user_input['velocity'],
        user_input['heading'],
        10
    )

    new_flight = {
        'icao24': 'manual',
        'callsign': user_input['callsign'],
        'lat': new_lat,
        'lon': new_lon,
        'alt': user_input['alt']
    }

    conflict_list = []

    for _, row in existing_df.iterrows():
        f_lat, f_lon = predict_position(row['latitude'], row['longitude'], row['velocity'], row['heading'], 10)
        other_flight = {
            'icao24': row['icao24'],
            'callsign': row['callsign'],
            'lat': f_lat,
            'lon': f_lon,
            'alt': row['baro_altitude']
        }

        if is_conflict(new_flight, other_flight):
            conflict_list.append(row['callsign'])

    with right_col:
        st.markdown("<h3 style='font-size: 22px;'>🚨 Conflict Detection Result</h3>", unsafe_allow_html=True)

        st.write(f"**Predicted Position (10 min):** `{round(new_lat, 4)}, {round(new_lon, 4)}`")

        if conflict_list:
            st.error(f"⚠️ Conflict Detected with: {', '.join(conflict_list)}")
        else:
            st.success("✅ No Conflict Detected for the Entered Flight.")
