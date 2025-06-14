import streamlit as st
import pandas as pd
import joblib

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
