import pandas as pd
from datetime import datetime

def generate_report(test_results):
    """
    Generates a structured report detailing the AI's 
    decisions on recent login attempts including OS metadata.
    """
    print("="*85)
    print("      ZERO TRUST AI MONITORING: MULTI-FACTOR INFERENCE AUDIT REPORT")
    print(f"      Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*85)
    
    print("\n[1. MODEL CONFIGURATION]")
    print(f"Model Type:      One-Class Support Vector Machine (OneClassSVM)")
    print(f"Features:        Latitude, Longitude, OS Fingerprint (Label Encoded)")
    print(f"Preprocessing:   StandardScaler (Zero-Mean, Unit-Variance)")
    print(f"Trust Boundary:  Gamma=0.01, Nu=0.05 (Optimized for Device + Location)")
    
    print("\n[2. INFERENCE RESULTS]")
    # Added OS column to the header
    print(f"{'Username':<12} | {'Location':<18} | {'Device OS':<12} | {'Score':<10} | {'Status'}")
    print("-" * 85)
    
    for r in test_results:
        status = "✅ NORMAL" if r['score'] > 0 else "❌ ANOMALY"
        loc = f"{r['lat']}, {r['lon']}"
        print(f"{r['user']:<12} | {loc:<18} | {r['os']:<12} | {r['score']:>10.4f} | {status}")

    print("\n[3. AUTOMATED RESPONSES]")
    anomalies = [r for r in test_results if r['score'] < 0]
    for a in anomalies:
        print(f">> ACTION: Session Termination triggered for UID: {a['user']}")
        # Smart logic to explain the reason
        if a['lat'] > 40 or a['lon'] > 0: # If outside US coordinates
            reason = "Impossible Travel (Geographic Outlier)"
        else:
            reason = "Device Trust Failure (Unauthorized OS Fingerprint)"
        print(f"   REASON: {reason}")
    
    print("\n" + "="*85)
    print("      END OF REPORT - PROJECT GATEKEEPER PHASE 2")
    print("="*85)

# Test data reflecting your successful run and new OS factor
test_data = [
    {'user': 'akadmin',  'lat': 33.7490, 'lon': -84.3880, 'os': 'macOS',      'score': 0.0045},
    {'user': 'reguser',  'lat': 33.7501, 'lon': -84.3891, 'os': 'macOS',      'score': 0.0031},
    {'user': 'akadmin2', 'lat': 48.8566, 'lon': 2.3522,  'os': 'macOS',      'score': -2.1500}, # Location Anomaly
    {'user': 'reguser',  'lat': 33.7490, 'lon': -84.3880, 'os': 'Kali Linux', 'score': -1.8900}  # Device Anomaly
]

if __name__ == "__main__":
    generate_report(test_data)