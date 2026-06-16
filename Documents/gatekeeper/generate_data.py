import pandas as pd
import random
from datetime import datetime, timedelta

# define user pool
users = ["akadmin", "reguser", "akadmin2"]
# define OS list
os_list = ["Windows 10", "Windows 11", "macOS", "Linux", "Android", "iOS"]
os_weights = [2, 5, 90, 1, 1, 1]  # more logins from Windows and macOS

data = []
for i in range(1000):
    # Pick a random user for this log entry
    current_user = random.choice(users)
    user_os = random.choices(os_list, weights=os_weights)[0]
    
    # simulate normal login timing
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 10000))
    
    # Atlanta coordinates (Your "Normal" baseline)
    lat = 33.7490
    lon = -84.3880
    
    # ADDING SOME REALISM: 
    # reguser may occasionally log in from a nearby city
    # so the AI learns a "zone" of trust rather than just one single point
    if current_user == "reguser" and random.random() > 0.8:
        lat += 0.01  
        lon += 0.01
    if current_user == "akadmin2" and random.random() > 0.9:
        lat += 0.02  
        lon += 0.02

    data.append({
        "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        "username": current_user, # Uses the randomly picked user
        "ip": "127.0.0.1", 
        "lat": lat,
        "lon": lon,
        "is_anomaly": 0,
        "os": user_os
    })
    
    # add a single anomaly for testing
data.append({
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "username": "attacker_pro",
    "ip": "1.1.1.1", 
    "lat": 0.0, # The Equator (Far from Atlanta!)
    "lon": 0.0, 
    "os": "Kali linux",
    "is_anomaly": 1  
})
df = pd.DataFrame(data)
df.to_csv("training_logs.csv", index=False)
print(f"Created training_logs.csv with 1,000 events for {', '.join(users)}.")

