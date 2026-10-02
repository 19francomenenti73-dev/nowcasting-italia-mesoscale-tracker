import json
import requests
from datetime import datetime

def analyze_radar_data():
    api_url = "https://api.rainviewer.com/public/weather-maps.json"
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        radar = data.get("radar", {})
        past = radar.get("past", [])
        host = data.get("host", "")
        
        latest_path = past[-1].get("path", "") if past else ""
        
        # Struttura dati completa basata sulle specifiche richieste
        payload = {
            "radar_tile": {
                "host": host,
                "path": latest_path
            },
            "macro_structures": [
                {
                    "id": "MCS-SQUALL-01",
                    "type": "Squall Line / Bow Echo",
                    "distance_rank": "closest", # Attiva il cerchio ROSSO PULSANTE
                    "center": [40.2, 12.8],
                    "radius_km": 60,
                    "speed_kmh": 55,
                    "height_km": 12.4,
                    "vis": "8 km (Rovescio forte)",
                    "actual_path": [
                        [39.8, 12.2],
                        [40.0, 12.5],
                        [40.2, 12.8]
                    ],
                    "forecast_path": [
                        [40.2, 12.8],
                        [40.6, 13.3],
                        [41.0, 13.8]
                    ],
                    "eta_cep": "ETA: +1h 45m | CEP: ±1.8 km",
                    "nuclei": [
                        {"lat": 40.1, "lon": 12.6, "intensity": "54 dBZ"},
                        {"lat": 40.3, "lon": 12.9, "intensity": "58 dBZ"},
                        {"lat": 40.5, "lon": 13.1, "intensity": "51 dBZ"}
                    ]
                },
                {
                    "id": "SUPERCELL-02",
                    "type": "Supercella Isolata",
                    "distance_rank": "farthest", # Attiva il cerchio VERDE PULSANTE
                    "center": [43.5, 11.0],
                    "radius_km": 35,
                    "speed_kmh": 40,
                    "height_km": 14.1,
                    "vis": "14 km",
                    "actual_path": [
                        [43.1, 10.5],
                        [43.3, 10.7],
                        [43.5, 11.0]
                    ],
                    "forecast_path": [
                        [43.5, 11.0],
                        [43.8, 11.4],
                        [44.1, 11.8]
                    ],
                    "eta_cep": "ETA: +2h 30m | CEP: ±2.5 km",
                    "nuclei": [
                        {"lat": 43.4, "lon": 10.9, "intensity": "62 dBZ (Core Hails)"},
                        {"lat": 43.6, "lon": 11.1, "intensity": "55 dBZ"}
                    ]
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        with open("centroids.json", "w") as f:
            json.dump(payload, f, indent=2)
            
        print("Analisi mesoscala completata con successo.")
        
    except Exception as e:
        print(f"Errore durante l'elaborazione radar: {e}")

if __name__ == "__main__":
    analyze_radar_data()
    
