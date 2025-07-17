import os
import pandas as pd

def limpiar_dataset(input_file, output_file):

    df = pd.read_csv(input_file, encoding='latin1')

    df_sin_nulos = df.dropna()

    df_sin_nulos.to_csv(output_file, index=False)
    print(f"Archivo limpio guardado en: {output_file}")





def procesar_carpeta(origen, destino):

    os.makedirs(destino, exist_ok=True)

    for archivo in os.listdir(origen):
        if archivo.endswith('.csv') and '_events' not in archivo:
            ruta_entrada = os.path.join(origen, archivo)
            nombre_salida = archivo.replace('.csv', '_1.csv')
            ruta_salida = os.path.join(destino, nombre_salida)
            limpiar_dataset(ruta_entrada, ruta_salida)




if __name__ == "__main__":
    
    carpeta_origen = "0_datos_brutos"
    carpeta_destino = "1_datos_limpios"
    procesar_carpeta(carpeta_origen, carpeta_destino)