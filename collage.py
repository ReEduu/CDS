from PIL import Image, ImageDraw, ImageFont
import os

def create_collage(folder_name):
    # Obtener la lista de nombres de archivo de las imágenes en la carpeta
    lista_imagenes = [imagen for imagen in os.listdir(folder_name) if imagen.endswith('.jpg') or imagen.endswith('.png')]

    # Tamaño de las imágenes en el collage
    imagen_size = (512, 512)

    # Tamaño del collage final (4x7 imágenes)
    collage_size = (imagen_size[0] * 4 + 200, imagen_size[1] * 7 + 100)  # Agregamos margen

    # Crear un lienzo en blanco para el collage
    collage = Image.new('RGB', collage_size, (255, 255, 255))

    # Fuente para los textos (ajustada para mejor visualización)
    font_size = 70
    font = ImageFont.truetype('Arial.ttf', font_size)

    # Textos para columnas y filas
    column_text = ['skull', 'vase', 'clock', 'background']
    row_text = ['anger', 'happiness', 'fear', 'neutral', 'surprise', 'sadness', 'disgust']

    # Diccionario para mapear los nombres de las imágenes a sus posiciones en el collage
    image_positions = {(column, row): None for column in column_text for row in row_text}

    # Llenar el diccionario con las imágenes correspondientes
    for imagen_nombre in lista_imagenes:
        if imagen_nombre.endswith('.png'):
            column, row = imagen_nombre[:-4].split('_')
            column_index = column_text.index(column)
            row_index = row_text.index(row)
            image_positions[(column_index, row_index)] = os.path.join(folder_name, imagen_nombre)

    # Iterar sobre las posiciones y colocar las imágenes en el collage
    for (column, row), imagen_path in image_positions.items():
        if imagen_path:
            # Abrir la imagen
            imagen = Image.open(imagen_path)

            # Calcular las coordenadas de la esquina superior izquierda de la imagen en el collage
            x = column * imagen_size[0] + 200  # Margen izquierdo
            y = row * imagen_size[1] + 100    # Margen superior

            # Pegar la imagen en el collage
            collage.paste(imagen, (x, y))

    # Dibujar los textos de las columnas y filas
    draw = ImageDraw.Draw(collage)
    column_text_spacing = 250  # Margen izquierdo
    for i, text in enumerate(column_text):
        x = i * imagen_size[0] + column_text_spacing
        y = 10
        draw.text((x, y), text, font=font, fill=(0, 0, 0))

    row_text_spacing = 250  # Margen superior
    for i, text in enumerate(row_text):
        x = 10
        y = i * imagen_size[1] + row_text_spacing
        rotated_text = Image.new('RGB', font.getbbox(text)[2:], (255, 255, 255))
        rotated_draw = ImageDraw.Draw(rotated_text)
        rotated_draw.text((0, 0), text, font=font, fill=(0, 0, 0))
        rotated_text = rotated_text.rotate(90, expand=True)
        collage.paste(rotated_text, (x, y))

    # Guardar el collage resultante
    collage.save('collage_resultante_con_textos.jpg')
    collage.show()

# Llamada a la función principal
create_collage('test_1')
