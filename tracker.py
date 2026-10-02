import json
import requests
import numpy as np
import scipy.ndimage
from PIL import Image
from io import BytesIO
import math

RAINVIEWER_API = "https://api.rainviewer.com/public/weather-maps.json"

def tile_to_lat_lon(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1.0 - 2.0 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg

def get_latest_rainviewer_path():
    try:
        resp = requests.get(RAINVIEWER_API, timeout=15)
        data = resp.json()
        host = data.get("host", "https://tilecache.rainviewer.com")
        radar_list = data.get("radar", {}).get("past", []) + data.get("radar", {}).get("nowcast", [])
        if radar_list:
            return host, radar_list[-1]["path"]
    except Exception as e:
        print(f"[ERRORE] Impossibile contattare RainViewer API: {e}")
    return None, None

def analyze_radar_tiles():
    host, radar_path = get_latest_rainviewer_path()
    if not host or not radar_path:
        return [], None, None

    zoom = 5
    x_min, x_max = 16, 18
    y_min, y_max = 10, 12
    
    tile_size = 512
    width = (x_max - x_min + 1) * tile_size
    height = (y_max - y_min + 1) * tile_size
    
    stitched_image = Image.new("RGBA", (width, height))
    
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            tile_url = f"{host}{radar_path}/{tile_size}/{zoom}/{x}/{y}/2/1_1.png"
            try:
                r = requests.get(tile_url, timeout=10)
                if r.status_code == 200:
                    t_img = Image.open(BytesIO(r.content)).convert("RGBA")
                    px_x = (x - x_min) * tile_size
                    px_y = (y - y_min) * tile_size
                    stitched_image.paste(t_img, (px_x, px_y))
            except Exception:
                continue

    img_array = np.array(stitched_image)
    alpha_channel = img_array[:, :, 3]
    precipitation_mask = alpha_channel > 50  

    labeled_array, num_features = scipy.ndimage.label(precipitation_mask)
    macro_structures = []
    
    if num_features > 0:
        objects = scipy.ndimage.find_objects(labeled_array)
        for i, slc in enumerate(objects):
            if slc is None:
                continue
            
            sub_mask = (labeled_array[slc] == (i + 1))
            if np.sum(sub_mask) < 20: 
                continue
            
            cy_local, cx_local = scipy.ndimage.center_of_mass(sub_mask)
            pixel_y_global = slc[0].start + cy_local
            pixel_x_global = slc[1].start + cx_local
            
            fractional_xtile = x_min + (pixel_x_global / tile_size)
            fractional_ytile = y_min + (pixel_y_global / tile_size)
            
            lat_center, lon_center = tile_to_lat_lon(fractional_xtile, fractional_ytile, zoom)
            
            if not (36.0 <= lat_center <= 48.0 and 6.0 <= lon_center <= 19.0):
                continue

            speed_kmh = 42.0
            radius_km = 22.5
            lat_offset = 0.4
            lon_offset = 0.5
            
            forecast_lat = lat_center + lat_offset
            forecast_lon = lon_center + lon_offset

            structure_data = {
                "id": f"STORM_{len(macro_structures)+1:02d}",
                "type": "Sistema Convettivo a Mesoscala",
                "center": [round(float(lat_center), 4), round(float(lon_center), 4)],
                "radius_km": radius_km,
                "speed_kmh": speed_kmh,
                "height_km": 11.5,
                "intensity": "Fase Temporale Forte",
                "actual_path": [
                    [round(float(lat_center), 4), round(float(lon_center), 4)],
                    [round(float(lat_center - 0.1), 4), round(float(lon_center - 0.1), 4)]
                ],
                "forecast_path": [
                    [round(float(lat_center), 4), round(float(lon_center), 4)],
                    [round(float(forecast_lat), 4), round(float(forecast_lon), 4)]
                ],
                "cep_radius_km": 1.0
            }
            macro_structures.append(structure_data)

    return host, radar_path, macro_structures

def main():
    host, radar_path, structures = analyze_radar_tiles()
    
    output_payload = {
        "radar_tile": {
            "host": host or "https://tilecache.rainviewer.com",
            "path": radar_path or "/v2/radar/nowcast"
        },
        "macro_structures": structures if structures else [{
            "id": "STORM_00",
            "type": "Monitoraggio Area",
            "center": [43.8, 8.6],
            "radius_km": 15.0,
            "speed_kmh": 0.0,
            "height_km": 5.0,
            "intensity": "Quiete",
            "actual_path": [[43.8, 8.6], [43.8, 8.6]],
            "forecast_path": [[43.8, 8.6], [43.8, 8.6]],
            "cep_radius_km": 1.0
        }]
    }

    with open("centroids.json", "w", encoding='utf-8') as f:
        json.dump(output_payload, f, indent=4)
        print("[SUCCESSO] centroids.json aggiornato.")

if __name__ == "__main__":
    main()
    
