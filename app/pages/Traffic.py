

# import pandas as pd
# import numpy as np
# from sklearn.cluster import DBSCAN
# import streamlit as st
# import plotly.express as px

# st.set_page_config(page_title="Flight Congestion Check", layout="centered")
# st.title("🛬 Check Air Traffic Congestion ")

# # -------------------------------
# # User Input for one flight
# # -------------------------------
# st.markdown("### ✈️ Enter Your Flight Details")
# with st.form("flight_form"):
#     flight_name = st.text_input("Flight Name", value="AI202")
#     user_lat = st.number_input("Latitude", format="%.6f", value=19.092100)
#     user_lon = st.number_input("Longitude", format="%.6f", value=72.862000)
#     submitted = st.form_submit_button("Check Congestion")

# # -------------------------------
# # Run logic after submission
# # -------------------------------
# if submitted:
#     # Generate 20 random nearby traffic points
#     np.random.seed(42)
#     lat_noise = np.random.normal(loc=user_lat, scale=0.01, size=20)
#     lon_noise = np.random.normal(loc=user_lon, scale=0.01, size=20)
#     traffic_df = pd.DataFrame({
#         'latitude': lat_noise,
#         'longitude': lon_noise,
#         'flight_name': [f'Traffic-{i}' for i in range(1, 21)]
#     })

#     # Add user's flight
#     user_df = pd.DataFrame({
#         'latitude': [user_lat],
#         'longitude': [user_lon],
#         'flight_name': [flight_name]
#     })

#     # Combine and run DBSCAN
#     df = pd.concat([traffic_df, user_df], ignore_index=True)
#     clustering = DBSCAN(eps=0.01, min_samples=3).fit(df[['latitude', 'longitude']])
#     df['cluster'] = clustering.labels_

#     # Get user's cluster
#     user_cluster = df.iloc[-1]['cluster']

#     # Map
#     fig = px.scatter_mapbox(
#         df,
#         lat="latitude",
#         lon="longitude",
#         color=df['cluster'].astype(str),
#         hover_name="flight_name",
#         zoom=10,
#         height=500
#     )
#     fig.update_layout(mapbox_style="open-street-map")
#     st.plotly_chart(fig)

#     # Result
#     if user_cluster == -1:
#         st.success(f"🟢 Flight **{flight_name}** is NOT in a congested area.")
#     else:
#         st.error(f"🔴 Flight **{flight_name}** IS in a congested area (Cluster {user_cluster}).")

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Flight Congestion Check", layout="wide")
st.title("🛬 Check Air Traffic Congestion")

# Create columns for layout
col1, col2 = st.columns([1, 2])  # Adjust ratio as needed

with col1:
    st.markdown("### ✈️ Enter Your Flight Details")
    with st.form("flight_form"):
        flight_name = st.text_input("Flight Name", value="AI202")
        user_lat = st.number_input("Latitude", format="%.6f", value=19.092100)
        user_lon = st.number_input("Longitude", format="%.6f", value=72.862000)
        submitted = st.form_submit_button("Check Congestion")

# Run logic after submission
if submitted:
    # Generate 20 random nearby traffic points
    np.random.seed(42)
    lat_noise = np.random.normal(loc=user_lat, scale=0.01, size=20)
    lon_noise = np.random.normal(loc=user_lon, scale=0.01, size=20)
    traffic_df = pd.DataFrame({
        'latitude': lat_noise,
        'longitude': lon_noise,
        'flight_name': [f'Traffic-{i}' for i in range(1, 21)]
    })

    # Add user's flight
    user_df = pd.DataFrame({
        'latitude': [user_lat],
        'longitude': [user_lon],
        'flight_name': [flight_name]
    })

    # Combine and run DBSCAN
    df = pd.concat([traffic_df, user_df], ignore_index=True)
    clustering = DBSCAN(eps=0.01, min_samples=3).fit(df[['latitude', 'longitude']])
    df['cluster'] = clustering.labels_

    # Get user's cluster
    user_cluster = df.iloc[-1]['cluster']

    with col2:
        # Map
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color=df['cluster'].astype(str),
            hover_name="flight_name",
            zoom=10,
            height=500
        )
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)

    # Result
    with col1:
        if user_cluster == -1:
            st.success(f"🟢 Flight **{flight_name}** is NOT in a congested area.")
        else:
            st.error(f"🔴 Flight **{flight_name}** IS in a congested area (Cluster {user_cluster}).")
