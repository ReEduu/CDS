import cv2
import time

# Lista de rutas de las imágenes
image_paths = ["clock_anger.png","clock_fear.png","clock_neutral.png"]

# Inicializa el índice de la imagen actual
current_image_index = 0

# Configura la ventana de OpenCV
cv2.namedWindow("Imagen")

while True:
    # Carga la imagen actual
    img_path = image_paths[current_image_index]
    img = cv2.imread(img_path)

    if img is not None:
        # Muestra la imagen
        cv2.imshow("Imagen", img)

        # Espera durante un tiempo (puedes ajustar el tiempo de visualización)
        key = cv2.waitKey(2000)

        # Cierra la ventana
        cv2.destroyWindow("Imagen")

        # Incrementa el índice para pasar a la siguiente imagen
        current_image_index += 1

        # Si alcanza el final de la lista de imágenes, vuelve al principio
        if current_image_index == len(image_paths):
            current_image_index = 0
    else:
        print("Fin de la presentación de imágenes.")
        break

# Cierra la ventana y finaliza el programa
cv2.destroyAllWindows()
