import os
import random

def generate_random_mask_path(img_path):
    img_directory = os.path.dirname(img_path)
    img_directory = os.path.dirname(img_directory)  
    masks_directory = os.path.join(img_directory, "mascaras")
    
    mask_names = [file for file in os.listdir(masks_directory) if not file.startswith(".")]
    if not mask_names:
        return None  # No hay máscaras disponibles
    print(mask_names)
    random_mask_name = random.choice(mask_names)
    mask_path = os.path.join(masks_directory, random_mask_name)
    return mask_path

# Ejemplo de uso
img_path = "imagenes/paint/imagenes/paint.jpg"
random_mask_path = generate_random_mask_path(img_path)
if random_mask_path:
    print(random_mask_path)
else:
    print("No hay máscaras disponibles en la carpeta.")
