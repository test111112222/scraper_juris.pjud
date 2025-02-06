import os

def combinar_archivos(directorio_raiz, archivo_salida):
    # Lista de archivos permitidos
    archivos_permitidos = {'crud.py', 'models.py', 'schemas.py', 'scraper.py'}

    with open(archivo_salida, 'w') as archivo_final:
        for root, _, files in os.walk(directorio_raiz):
            for file in files:
                # Verificar si el archivo está en la lista de permitidos
                if file in archivos_permitidos:
                    ruta_completa = os.path.join(root, file)
                    try:
                        with open(ruta_completa, 'r') as archivo:
                            contenido = archivo.read()
                            archivo_final.write(f"=== Archivo: {ruta_completa} ===\n{contenido}\n\n")  # Agrega un salto de línea entre archivos
                    except Exception as e:
                        print(f"Error al procesar {ruta_completa}: {e}")

if __name__ == "__main__":
    directorio_raiz = '.'  # Directorio raíz donde buscar los archivos
    archivo_salida = 'combinado.txt'  # Nombre del archivo de salida
    combinar_archivos(directorio_raiz, archivo_salida)
    print(f"Archivos combinados en {archivo_salida}")