import os
import shutil
from PyPDF2 import PdfReader

def extraer_metadatos(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        lector_pdf = PdfReader(pdf_file)
        metadatos = lector_pdf.metadata
        autor = metadatos.get('/Author', 'Desconocido')
        titulo = metadatos.get('/Title', 'Sin_titulo')
    return autor, titulo

def renombrar_archivos(directorio_base):
    carpeta_no_renombrados = os.path.join(directorio_base, 'no_renombrados')
    os.makedirs(carpeta_no_renombrados, exist_ok=True)

    for archivo in os.listdir(directorio_base):
        ruta_archivo = os.path.join(directorio_base, archivo)

        if os.path.isfile(ruta_archivo) and archivo.lower().endswith('.pdf'):
            try:
                autor, titulo = extraer_metadatos(ruta_archivo)
                nuevo_nombre = f'{autor} - {titulo}.pdf'

                if autor != 'Desconocido' and titulo != 'Sin_titulo':
                    nuevo_path = os.path.join(directorio_base, nuevo_nombre)
                    os.rename(ruta_archivo, nuevo_path)
                    print(f'Renombrado: {ruta_archivo} -> {nuevo_path}')
                else:
                    nuevo_path = os.path.join(carpeta_no_renombrados, archivo)
                    shutil.move(ruta_archivo, nuevo_path)
                    print(f'No se pudo renombrar, movido a {nuevo_path}')

            except Exception as e:
                print(f'Error al procesar {ruta_archivo}: {e}')

    eliminar_carpetas_vacias(directorio_base)

def eliminar_carpetas_vacias(directorio):
    for root, dirs, files in os.walk(directorio, topdown=False):
        for carpeta in dirs:
            carpeta_actual = os.path.join(root, carpeta)
            if not os.listdir(carpeta_actual):
                os.rmdir(carpeta_actual)
                print(f'Eliminada carpeta vacía: {carpeta_actual}')

# Ruta al directorio donde se encuentran los archivos PDF
directorio_base = r'C:\Users\paula\OneDrive\Escritorio\libros'

# Llamar a la función para renombrar los archivos
renombrar_archivos(directorio_base)
