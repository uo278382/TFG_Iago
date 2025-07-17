import os
import glob
import pandas as pd
import numpy as np

os.makedirs('4_instantes_elegidos', exist_ok=True)

archivos = glob.glob('3_datos_sin_columnas/*_3.csv')

for archivo in archivos:
    df = pd.read_csv(archivo)
    nuevo_df = pd.DataFrame()

    for event_id, grupo in df.groupby('event_id'):
        total_filas = len(grupo)

        if total_filas < 40:
            print(f"Evento {event_id} en {os.path.basename(archivo)} tiene menos de 40 filas, se omite")
            continue



        indices = np.linspace(0, total_filas - 1, 40, dtype=int)
        grupo_seleccionado = grupo.iloc[indices]
        
        nuevo_df = pd.concat([nuevo_df, grupo_seleccionado], ignore_index=True)



    nombre_base = os.path.basename(archivo)
    nuevo_nombre = nombre_base.replace('_3.csv', '_4.csv')
    salida = os.path.join('4_instantes_elegidos', nuevo_nombre)



    nuevo_df.to_csv(salida, index=False)

    print(f"{nombre_base} procesado y guardado como {salida}")