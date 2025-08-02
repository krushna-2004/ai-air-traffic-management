import numpy as np
from haversine import haversine

def predict_position(lat, lon, speed, heading, minutes_ahead):
    """
    Predict future position using current lat/lon, speed (m/s), and heading (degrees)
    """
    R = 6371e3  # Earth radius in meters
    distance = speed * 60 * minutes_ahead
    heading_rad = np.radians(heading)

    lat1 = np.radians(lat)
    lon1 = np.radians(lon)

    lat2 = np.arcsin(np.sin(lat1) * np.cos(distance / R) +
                     np.cos(lat1) * np.sin(distance / R) * np.cos(heading_rad))

    lon2 = lon1 + np.arctan2(np.sin(heading_rad) * np.sin(distance / R) * np.cos(lat1),
                             np.cos(distance / R) - np.sin(lat1) * np.sin(lat2))

    return np.degrees(lat2), np.degrees(lon2)

def is_conflict(ac1, ac2):
    """
    Check if two aircraft will conflict: <5nm horizontal & <1000ft vertical
    """
    horizontal_dist = haversine((ac1['lat'], ac1['lon']), (ac2['lat'], ac2['lon'])) * 1000
    vertical_sep = abs(ac1['alt'] - ac2['alt'])

    return horizontal_dist < 9260 and vertical_sep < 305
