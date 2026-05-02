import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_large_dataset(filename, num_assets=15, days=365):
    np.random.seed(42)
    start_date = datetime(2023, 1, 1)
    data = []

    asset_types = ['CRITICAL', 'RELIABLE', 'NORMAL', 'WEAR_OUT', 'INFANT_MORTALITY']
    
    for i in range(num_assets):
        asset_id = f"EQ-{i+1:03d}"
        a_type = np.random.choice(asset_types)
        
        current_time = start_date
        total_hours = 0
        
        while current_time < start_date + timedelta(days=days):
            # Determinamos el MTBF basado en el tipo de activo
            if a_type == 'RELIABLE':
                mtbf_hours = np.random.normal(800, 100)
                mttr_hours = np.random.normal(2, 0.5)
            elif a_type == 'CRITICAL':
                mtbf_hours = np.random.normal(150, 30)
                mttr_hours = np.random.normal(24, 6)
            elif a_type == 'WEAR_OUT':
                # MTBF disminuye con el tiempo
                progress = (current_time - start_date).days / days
                mtbf_hours = max(50, 400 * (1 - progress))
                mttr_hours = np.random.normal(8, 2)
            elif a_type == 'INFANT_MORTALITY':
                # MTBF aumenta con el tiempo
                progress = (current_time - start_date).days / days
                mtbf_hours = min(600, 50 + 800 * progress)
                mttr_hours = np.random.normal(4, 1)
            else: # NORMAL
                mtbf_hours = np.random.normal(400, 50)
                mttr_hours = np.random.normal(5, 1)

            # Siguiente falla
            uptime = max(1, int(mtbf_hours))
            current_time += timedelta(hours=uptime)
            
            if current_time >= start_date + timedelta(days=days):
                break
                
            falla_time = current_time
            
            # Tiempo de reparación
            downtime = max(0.5, mttr_hours)
            current_time += timedelta(hours=downtime)
            reparacion_time = current_time
            
            data.append({
                'ID_Equipo': asset_id,
                'Fecha_Falla': falla_time.strftime('%Y-%m-%d %H:%M'),
                'Fecha_Reparacion': reparacion_time.strftime('%Y-%m-%d %H:%M'),
                'Horas_Operacion': uptime
            })

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"[INFO] Dataset con {len(df)} registros generado en '{filename}'.")

if __name__ == "__main__":
    generate_large_dataset('historial_fallas.csv')
