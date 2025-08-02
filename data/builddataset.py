import pandas as pd
import random
import time

def simulate_aircraft_positions(n=15):
    aircraft = []
    timestamp = int(time.time())  # current UNIX time
    
    for i in range(n):
        icao = f"ac{i:03d}"
        callsign = f"FL{random.randint(100, 999)}"
        
        # Simulate location roughly within India
        lat = round(random.uniform(8.0, 37.0), 4)
        lon = round(random.uniform(68.0, 97.0), 4)
        
        altitude = random.choice(range(30000, 40001, 1000))  # feet
        velocity = round(random.uniform(200, 280), 1)  # m/s (~720–1000 km/h)
        heading = random.randint(0, 359)
        
        aircraft.append({
            "icao24": icao,
            "callsign": callsign,
            "time": timestamp,
            "latitude": lat,
            "longitude": lon,
            "baro_altitude": altitude,
            "velocity": velocity,
            "heading": heading
        })
        
    return pd.DataFrame(aircraft)

# Generate and save to CSV
df = simulate_aircraft_positions(15)
df.to_csv("simulated_aircraft_positions.csv", index=False)
print("✅ Simulated dataset saved as 'simulated_aircraft_positions.csv'")
