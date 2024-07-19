import os
import openpyxl
import csv

def leer_libros(directorio_base):
    libros = []

    # Obtener la lista de categorías ordenadas
    categorias = sorted(os.listdir(directorio_base))

    # Recorrer las categorías ordenadas
    for categoria in categorias:
        categoria_ruta = os.path.join(directorio_base, categoria)

        # Verificar si es una subcarpeta (categoría)
        if os.path.isdir(categoria_ruta):
            for autor in os.listdir(categoria_ruta):
                autor_ruta = os.path.join(categoria_ruta, autor)

                # Verificar si es una subcarpeta (autor)
                if os.path.isdir(autor_ruta):
                    for archivo in os.listdir(autor_ruta):
                        archivo_ruta = os.path.join(autor_ruta, archivo)

                        # Verificar si es un archivo (sin importar la extensión)
                        if os.path.isfile(archivo_ruta):
                            autor_nombre, titulo = archivo.split(' - ', 1) if ' - ' in archivo else ('', '')
                            titulo_sin_extension, extension = os.path.splitext(titulo)
                            
                            # Verificar si el archivo es de interés (por ejemplo, pdf)
                            if extension.lower() in ['.pdf', '.epub', '.txt', '.docx']:
                                libros.append({
                                    'Autor': autor_nombre,
                                    'Título': titulo_sin_extension,
                                    'Categoría': categoria
                                })

    return libros

def guardar_en_excel_y_csv(libros, nombre_archivo_excel, nombre_archivo_csv):
    # Crear un nuevo archivo Excel
    libro_excel = openpyxl.Workbook()
    hoja_excel = libro_excel.active

    # Añadir encabezados a la hoja de Excel
    hoja_excel.append(['Autor', 'Título', 'Categoría'])

    # Agregar la información a la hoja de Excel
    for libro in libros:
        hoja_excel.append([libro['Autor'], libro['Título'], libro['Categoría']])

    # Guardar el archivo Excel
    libro_excel.save(nombre_archivo_excel)
    print(f'Índice Excel creado exitosamente: {os.path.abspath(nombre_archivo_excel)}')

    # Guardar el archivo CSV
    with open(nombre_archivo_csv, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Autor', 'Título', 'Categoría'])
        for libro in libros:
            csv_writer.writerow([libro['Autor'], libro['Título'], libro['Categoría']])

    print(f'Índice CSV creado exitosamente: {os.path.abspath(nombre_archivo_csv)}')

# Solicitar la ruta del directorio base
directorio_base = input("Por favor, ingresa la ruta del directorio base: ")

# Obtener la lista de libros
libros = leer_libros(directorio_base)

# Guardar en Excel y CSV
nombre_archivo_excel = 'indice_libros.xlsx'
nombre_archivo_csv = 'indice_libros.csv'
guardar_en_excel_y_csv(libros, nombre_archivo_excel, nombre_archivo_csv)
