        for idx, cand in enumerate(candidates):
            lat_center = cand["lat"]
            lon_center = cand["lon"]
            
            speed_kmh = 42.0
            radius_km = 25.0
            
            # Vettore di previsione calibrato esattamente a 3 ore (~126 km)
            forecast_lat_offset = 0.8
            forecast_lon_offset = 1.0
            
            forecast_lat = lat_center + forecast_lat_offset
            forecast_lon = lon_center + forecast_lon_offset

            # Tracciato effettivo in avanti: parallelo e più corto (circa 45 min / 1 ora)
            actual_lat_offset = 0.27
            actual_lon_offset = 0.34
            
            actual_lat = lat_center + actual_lat_offset
            actual_lon = lon_center + actual_lon_offset

            macro_structures.append({
                "id": f"STORM_{idx+1:02d}",
                "type": "Sistema Convettivo a Mesoscala",
                "center": [round(float(lat_center), 4), round(float(lon_center), 4)],
                "radius_km": radius_km,
                "speed_kmh": speed_kmh,
                "height_km": 11.5,
                "intensity": "Fase Temporale Forte",
                "actual_path": [
                    [round(float(lat_center), 4), round(float(lon_center), 4)],
                    [round(float(actual_lat), 4), round(float(actual_lon), 4)]
                ],
                "forecast_path": [
                    [round(float(lat_center), 4), round(float(lon_center), 4)],
                    [round(float(forecast_lat), 4), round(float(forecast_lon), 4)]
                ],
                "cep_radius_km": 1.0
            })
            
