import json
import os
import requests

def main():
    url = "https://api.press/public/weather-maps.json" # o rainviewer
    # Usiamo l'endpoint ufficiale RainViewer
    api_url = "https://api.rainviewer.com/public/weather-maps.json"
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        radar = data.get("radar", {})
        past = radar.get("past", [])
        
        centroids = []
        if past:
            latest = past[-1]
            centroids.append({
                "time": latest.get("time"),
                "path": latest.get("path"),
                "host": data.get("host", ""),
                "status": "active"
            })
        
        with open("centroids.json", "w") as f:
            json.dump(centroids, f, indent=2)
        print("File centroids.json creato con successo.")
        
    except Exception as e:
        print(f"Errore durante il recupero: {e}")
        # Crea comunque un file vuoto per evitare errori di git
        with open("centroids.json", "w") as f:
            json.dump([], f)

if __name__ == "__main__":
    main()
    
