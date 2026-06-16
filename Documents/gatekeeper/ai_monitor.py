import pandas as pd
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import LabelEncoder, StandardScaler
import requests
import matplotlib.pyplot as plt
import numpy as np

# 1. Load and train
train_df = pd.read_csv("training_logs.csv")
le = LabelEncoder()
train_df['os_encoded'] = le.fit_transform(train_df['os'])

# scale the data
scaler = StandardScaler()
train_scaled = scaler.fit_transform(train_df[['lat', 'lon', 'os_encoded']])
# kernel defines the shape of the decision boundary (RBF is common for non-linear data)
# nu defines the proportion of outliers we expect
# gamma defines how tight the circle is
model = OneClassSVM(kernel='rbf', gamma=0.01, nu=0.05)
model.fit(train_scaled)

# 2. The "Threat" Simulation function
def evaluate_login(username, ip, lat, lon, os_name):
    # wrap the test data in a DataFrame with matching column names
    os_encoded = le.transform([os_name])[0] if os_name in le.classes_ else 99    
    test_point = pd.DataFrame([[lat, lon, os_encoded]], columns=['lat', 'lon', 'os_encoded'])
    test_scaled = scaler.transform(test_point)  # scale using the same scaler as training
    
    score = model.decision_function(test_scaled)[0]
    prediction = model.predict(test_scaled)[0]  # -1 for anomaly, 1 for normal
    
    if prediction == -1:  # If the score is negative, it's an anomaly
        print(f"\n!!!ALERT: Travel Anomaly detected for {username} (Score: {score:.4f})!!!")
        print(f"Location: ({lat}, {lon}) is OUTSIDE the trust zone.")
        trigger_lockdown(username)
    else:
        print(f"Login for {username} at ({lat}, {lon}) looks normal. (Score: {score:.4f})")

# 3. The "Action" (Calling Authentik API)
def trigger_lockdown(username):
    if username == "akadmin":
        print(f"[SAFEGUARD] Admin anomaly ignored.")
        return
    
    token = "TIv7osu9qP2d5DwyY6pqj5Cg60YMXdnihhjrqoEpIZplf4dbPNQcXCEtqUq8"
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. find the User
    user_url = f"http://localhost:9000/api/v3/core/users/?username={username}"
    user_resp = requests.get(user_url, headers=headers)
    user_data = user_resp.json()
    
    if not user_data.get('results'):
        print(f"!!! Error: User {username} not found.")
        return

    user_id = user_data['results'][0]['pk']
    
    # 2. THE "TOGGLE" ACTION (This is what you're missing!)
    # this flips the 'Is Active' switch to False in Authentik
    print(f"[SECURITY ACTION] Deactivating account toggle for: {username}")
    patch_url = f"http://localhost:9000/api/v3/core/users/{user_id}/"
    patch_resp = requests.patch(patch_url, json={"is_active": False}, headers=headers)

    if patch_resp.status_code == 200:
        print(f">>> SUCCESS: {username} is now INACTIVE in the dashboard.")
    else:
        print(f"!!! Failed to flip toggle: {patch_resp.status_code}")

    # 3. kill the current session (Optional but helps the 'kick out')
    session_url = f"http://localhost:9000/api/v3/core/authenticated_sessions/?user={user_id}"
    session_resp = requests.get(session_url, headers=headers)
    results = session_resp.json().get('results', [])
    
    for session in results:
        s_id = session.get('pk')
        requests.delete(f"http://localhost:9000/api/v3/core/authenticated_sessions/{s_id}/", headers=headers)
        print(f">>> SUCCESS: Active session {s_id} terminated.")


# 1. Plot the training data (The "Trust Zone")
plt.scatter(train_df['lon'], train_df['lat'], c='blue', label='Normal (Atlanta)')

# 2. Plot the attack points
plt.scatter(2.3522, 48.8566, c='red', marker='x', s=100, label='Attack (Paris)')
plt.scatter(139.6917, 35.6895, c='orange', marker='x', s=100, label='Attack (Tokyo)')

plt.title("AI Detection: Geographical Outlier Analysis")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.show()

# --- THE TEST SUITE ---
print("--- Testing Normal Logins ---")
evaluate_login("akadmin", "127.0.0.1", 33.7490, -84.3880, "macOS")
evaluate_login("reguser", "127.0.0.1", 33.7501, -84.3891, "macOS")

print("\n--- Testing Anomaly Logins (The Threat) ---")
# simulate akadmin2 being compromised from Paris
evaluate_login("akadmin2", "192.168.1.50", 48.8566, 2.3522, "Linux")

# simulate reguser being compromised from Tokyo
evaluate_login("reguser", "203.0.113.5", 35.6895, 139.6917, "Windows 10")