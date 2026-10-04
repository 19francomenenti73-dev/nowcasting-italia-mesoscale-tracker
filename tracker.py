import json
import requests
from datetime import datetime

def get_latest_radar_tile():
    """Recupera l'ultimo path radar live dalle API pubbliche di RainViewer"""
    try:
        response = requests.get("https://api.rainviewer.com/public/weather-maps.json", timeout=10)
        data = response.json()
        host = data.get("host", "https://tilecache.rainviewer.com")
        past_frames = data.get("radar", {}).get("past", [])
        if past_frames:
            # Prende l'ultimo fotogramma disponibile
            latest = past_frames[-1]
            return {
                "host": host,
                "path": latest.get("path")
            }
    except Exception as e:
        print(f"Errore nel recupero del radar RainViewer: {e}")
    
    # Fallback di sicurezza se la chiamata fallisce
    return {
        "host": "https://tilecache.rainviewer.com",
        "path": "/v2/radar/1710000000"
    }

def generate_centroids_json():
    radar_info = get_latest_radar_tile()

    data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "radar_tile": radar_info,
        "macro_structures": [
            {
                "id": "TC-Liguria-01",
                "center": [44.25, 8.90],  # Latitudine e Longitudine del centroide
                "speed_kmh": 45,
                "intensity": "Moderata-Alta",
                "actual_path": [
                    [44.10, 8.70],
                    [44.15, 8.78],
                    [44.20, 8.84],
                    [44.25, 8.90]
                ],
                "forecast_path": [
                    [44.30, 8.96],
                    [44.35, 9.02],
                    [44.40, 9.08]
                ]
            }
        ]
    }

    # Salva il file JSON per il frontend
    with open("centroids.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("File centroids.json aggiornato con radar live e celle.")

if __name__ == "__main__":
    generate_centroids_json()
    
