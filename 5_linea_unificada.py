import pandas as pd
import os
import glob

carpeta_entrada = "4_instantes_elegidos"
carpeta_salida = "5_datos_1_linea"
os.makedirs(carpeta_salida, exist_ok=True)

columnas_ignorar = ['event_id', 'clase']

for ruta in glob.glob(os.path.join(carpeta_entrada, "*_4.csv")):

    nombre_archivo = os.path.basename(ruta)
    nombre_base = nombre_archivo.replace("_4.csv", "")
    salida = os.path.join(carpeta_salida, f"{nombre_base}_5.csv")


    print(f"Procesando {nombre_archivo} a {nombre_base}_5.csv")


    try:
        df = pd.read_csv(ruta)
    except pd.errors.EmptyDataError:
        print(f"El archivo {nombre_archivo} está vacío, se omite.")
        continue


    if 'clase' not in df.columns:
        raise ValueError(f"El archivo {ruta} no contiene columna clase")

    filas_finales = []



    for event_id, grupo in df.groupby("event_id"):

        clase = grupo.iloc[0]['clase']
        grupo_limpio = grupo.drop(columns=[col for col in columnas_ignorar if col in grupo.columns])
        valores = grupo_limpio.to_numpy().flatten().tolist()


        fila = [int(event_id), int(clase)] + valores
        filas_finales.append(fila)



    columnas_instantes = grupo_limpio.columns
    cabecera = ['event_id', 'clase']

    for i in range(len(grupo_limpio)):

        for col in columnas_instantes:
            cabecera.append(f"{col}_{i+1}")



    df_final = pd.DataFrame(filas_finales, columns=cabecera)

    df_final = df_final.dropna()


    df_final.to_csv(salida, index=False)

    print(f"Guardado en {salida}")