import json
from datetime import datetime

def generate_centroids_json():
    # Inserisci qui la tua logica di elaborazione radar (es. estrazione centroidi, calcolo velocità e percorsi)
    
    data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "macro_structures": [
            {
                "id": "TC-Liguria-01",
                "center": [44.25, 8.90],  # [Latitudine, Longitudine] del centroide
                "speed_kmh": 45,
                "intensity": "Moderata",
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

    # Scrive il file JSON nella cartella di lavoro
    with open("centroids.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("File centroids.json aggiornato con successo.")

if __name__ == "__main__":
    generate_centroids_json()
    
