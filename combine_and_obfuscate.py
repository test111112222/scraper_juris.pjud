import os

def combinar_archivos(directorio_raiz, archivo_salida):
    with open(archivo_salida, 'w') as archivo_final:
        for root, _, files in os.walk(directorio_raiz):
            for file in files:
                if file.endswith('.py'):
                    ruta_completa = os.path.join(root, file)
                    try:
                        with open(ruta_completa, 'r') as archivo:
                            contenido = archivo.read().replace("\n", "")
                            archivo_final.write(f"=== Archivo:{ruta_completa} ===\n{contenido}\n")
                    except Exception as e:
                        print(f"Error al procesar {ruta_completa}: {e}")

if __name__ == "__main__":
    directorio_raiz = '.'
    archivo_salida = 'combinado.txt'
    combinar_archivos(directorio_raiz, archivo_salida)
    print(f"Archivos combinados en {archivo_salida}")