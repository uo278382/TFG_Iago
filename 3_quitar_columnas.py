import pandas as pd
import os
import glob

os.makedirs('3_datos_sin_columnas', exist_ok=True)

input_files = glob.glob('2_datos_linea/*_2.csv')

for input_path in input_files:


    nombre_archivo = os.path.basename(input_path) 
    nombre_base = nombre_archivo.replace('_2.csv', '')


    nuevo_nombre = f"{nombre_base}_3.csv"
    output_path = os.path.join('3_datos_sin_columnas', nuevo_nombre)

    print(f"Procesando {nombre_archivo} a {nuevo_nombre}")


    df = pd.read_csv(input_path, encoding='latin1')



    columnas_eliminar = [
        "play_label", "event_time",
        "team_id_home", "team_id_away",
        "player_id_player_1", "player_id_player_2", "player_id_player_3", "player_id_player_4", "player_id_player_5",
        "player_id_player_6", "player_id_player_7", "player_id_player_8", "player_id_player_9", "player_id_player_10"
    ]



    df = df.drop(columns=[col for col in columnas_eliminar if col in df.columns])

    df.to_csv(output_path, index=False)