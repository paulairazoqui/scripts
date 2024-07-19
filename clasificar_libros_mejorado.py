import os
import shutil
from PyPDF2 import PdfReader

def extraer_metadatos(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        lector_pdf = PdfReader(pdf_file)
        metadatos = lector_pdf.metadata
        etiquetas = metadatos['/Keywords'].split(', ') if '/Keywords' in metadatos else []
        autores = metadatos['/Author'].split(', ') if '/Author' in metadatos else []
    return etiquetas, autores

def organizar_libros(directorio_base):
    # Recorremos todos los archivos en el directorio base
    for archivo in os.listdir(directorio_base):
        ruta_archivo = os.path.join(directorio_base, archivo)

        # Ignoramos los subdirectorios, solo procesamos archivos
        if os.path.isfile(ruta_archivo):
            try:
                # Leemos los metadatos del archivo PDF
                etiquetas, autores = extraer_metadatos(ruta_archivo)

                # Usamos solo la primera etiqueta (si hay alguna)
                primera_etiqueta = etiquetas[0] if etiquetas else None

                if primera_etiqueta:
                    # Creamos carpetas según la primera etiqueta
                    carpeta_etiqueta = os.path.join(directorio_base, primera_etiqueta)
                    os.makedirs(carpeta_etiqueta, exist_ok=True)

                    # Creamos carpetas según los autores dentro de la carpeta de la etiqueta
                    for autor in autores:
                        carpeta_autor = os.path.join(carpeta_etiqueta, autor)
                        os.makedirs(carpeta_autor, exist_ok=True)

                        # Construimos la ruta de destino
                        destino = os.path.join(carpeta_autor, archivo)

                        # Movemos o eliminamos el archivo según si ya existe
                        if not os.path.exists(destino):
                            shutil.move(ruta_archivo, destino)
                            print(f'Procesado: {ruta_archivo}')
                        else:
                            # Eliminamos el archivo existente
                            os.remove(ruta_archivo)
                            print(f'Eliminado duplicado: {ruta_archivo}')

            except Exception as e:
                print(f'Error al procesar {ruta_archivo}: {e}')

    # Eliminamos carpetas vacías al final del proceso
    eliminar_carpetas_vacias(directorio_base)

def eliminar_carpetas_vacias(directorio):
    for root, dirs, files in os.walk(directorio, topdown=False):
        for carpeta in dirs:
            carpeta_actual = os.path.join(root, carpeta)
            if not os.listdir(carpeta_actual):
                os.rmdir(carpeta_actual)
                print(f'Eliminada carpeta vacía: {carpeta_actual}')

# Ruta al directorio donde se encuentran los archivos renombrados
directorio_base = r'C:\Users\paula\OneDrive\Escritorio\Nueva Carpeta'

# Llamar a la función para organizar los libros
organizar_libros(directorio_base)
