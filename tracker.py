import os
import json
import requests
import numpy as np
from datetime import datetime, timezone
from scipy.ndimage import label, center_of_mass

# Configurazione aree e API RainViewer
RAINVIEWER_API = "https://www.rainviewer.com/api/v2/maps.json"
HISTORY_FILE = "history.json"
OUTPUT_FILE = "centroids.json"

def fetch_latest_radar():
    """Recupera l'ultimo timestamp disponibile dall'API di RainViewer."""
    response = requests.get(RAINVIEWER_API)
    if response.status_code == 200:
        data = response.json()
        past_frames = data.get("radar", {}).get("past", [])
        if past_frames:
            return past_frames[-1]["time"], past_frames[-1]["path"]
    return None, None

def classify_structure(area_size, max_dbz, elongation, has_rotation_signature):
    """Classifica la struttura basandosi sulla nomenclatura ufficiale italiana."""
    if max_dbz >= 55 and has_rotation_signature:
        return "Supercella"
    elif max_dbz >= 50 and elongation > 3.5:
        return "Linea di Squall / Linea di Groppo"
    elif max_dbz >= 48 and elongation > 2.5:
        return "Bow Echo (Eco a Arco)"
    elif area_size > 500 and max_dbz >= 45:
        return "MCS (Sistema Convettivo a Mesoscala)"
    elif area_size > 800:
        return "MCC (Complesso Convettivo Mesoscalico)"
    elif elongation > 3.0 and max_dbz >= 42:
        return "Testa a Virgola (Comma Head)"
    elif max_dbz >= 40 and area_size > 300:
        return "Cluster Multicellulare"
    elif max_dbz < 40 and area_size <= 100:
        return "Cella Unicellulare / Isolata"
    else:
        return "MCV (Mesoscale Convective Vortex)"

def main():
    print("Avvio motore di nowcasting radar...")
    timestamp, path = fetch_latest_radar()
    if not timestamp:
        print("Impossibile recuperare il timestamp radar.")
        return

    print(f"Ultimo frame radar valido trovato: {timestamp} (Path: {path})")

    current_time = datetime.now(timezone.utc).isoformat()
    
    # Struttura dati dimostrativa dei centroidi calcolati per l'Italia
    payload = {
        "timestamp": current_time,
        "radar_time": timestamp,
        "cores": [
            {
                "id": "ITA_CORE_01",
                "lat": 44.4056,
                "lon": 8.9463,
                "color": "red",
                "structure_type": "Supercella",
                "probability": 92,
                "max_height_km": 12.5,
                "max_dbz": 58,
                "velocity_kmh": 45.0,
                "heading_deg": 110,
                "vis": "Ridotta per grandine",
                "history_path": [
                    [44.4500, 8.8500],
                    [44.4300, 8.8900],
                    [44.4056, 8.9463]
                ],
                "predictive_vector": [
                    [44.4056, 8.9463],
                    [44.3500, 9.1000],
                    [44.2800, 9.2500]
                ],
                "eta_minutes": 145,
                "cep_radius_km": 12.4,
                "decay_status": "active"
            }
        ]
    }

    # Salvataggio del file JSON letto poi dal frontend
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)
        
    print(f"File {OUTPUT_FILE} generato e pronto per il commit automatico.")

if __name__ == "__main__":
    main()
