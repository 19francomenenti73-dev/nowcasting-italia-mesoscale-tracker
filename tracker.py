import json
import requests

def main():
    api_url = "https://api.rainviewer.com/public/weather-maps.json"
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        radar = data.get("radar", {})
        past = radar.get("past", [])
        host = data.get("host", "")
        
        centroids = []
        if past:
            latest = past[-1]
            centroids.append({
                "time": latest.get("time"),
                "path": latest.get("path"),
                "host": host,
                "status": "active"
            })
        
        with open("centroids.json", "w") as f:
            json.dump(centroids, f, indent=2)
        print("File centroids.json aggiornato con successo.")
        
    except Exception as e:
        print(f"Errore durante il recupero: {e}")
        with open("centroids.json", "w") as f:
            json.dump([], f)

if __name__ == "__main__":
    main()
