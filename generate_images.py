import os
import cv2
import numpy as np
import time
import torch
import csv
import tempfile
import matplotlib.pyplot as plt
import cv2
import sys
import PIL
import argparse
import pandas as pd
import subprocess
from matplotlib.animation import FuncAnimation
from datetime import datetime
from PIL import Image
from diffusers import StableDiffusionInpaintPipeline



def load_image(file_path):
    return PIL.Image.open(file_path).convert("RGB")

def generate_and_save_inpainting(img_path, mask_path, prompt, emocion_actual):

    image_name = os.path.splitext(os.path.basename(img_path))[0]

    print(image_name)
    
    # Crear una carpeta con el nombre de la imagen si no existe
    output_folder = os.path.join(".", image_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Construir el nombre del archivo de la imagen generada
    generated_image_name = f"{image_name}_{emocion_actual}.png"
    generated_image_path = os.path.join(output_folder, generated_image_name)

    
    # Verificar si la imagen ya fue generada anteriormente
    if not os.path.exists(generated_image_path):
        init_image = load_image(img_path).resize((512, 512))
        mask_image = load_image(mask_path).resize((512, 512))
        pipe = StableDiffusionInpaintPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-inpainting",
            torch_dtype=torch.float16,
            )
        pipe = pipe.to("mps")
        image = pipe(prompt=prompt, image=init_image, mask_image=mask_image, num_inference_steps=50).images[0]
        generated_image_name = f"{image_name}_{emocion_actual}.png"
        generated_image_path = os.path.join(output_folder, generated_image_name)


        # Guardar la imagen generada en la carpeta "imagenes generadas"
        generated_image_filename = f"{image_name}_{emocion_actual}.png"
        generated_image_save_path = os.path.join("imagenes","paint","imagenes generadas", generated_image_filename)
        print(generated_image_save_path)
        image.save(generated_image_save_path)

csv_path = "csv/descriptions.csv"

# Ruta de la carpeta donde se encuentra el código
base_folder = os.path.dirname(os.path.abspath(__file__))

# Leer el archivo CSV
df = pd.read_csv(csv_path)

# Columnas 1 y 2 corresponden a los nombres de las imágenes y máscaras
for index, row in df.iterrows():
    image_folder_name = row[0]
    
    # Ruta a la carpeta que contiene las imágenes y máscaras
    image_mask_folder = os.path.join(base_folder,"imagenes", image_folder_name)
    image_folder = os.path.join(image_mask_folder, "imagenes")
    mask_folder = os.path.join(image_mask_folder, "mascaras")
    
    # Ruta de la imagen base y la máscara
    base_image_path = os.path.join(image_folder, row[0] + ".jpg")
    mask_name = row[1] + "_mask.png"
    mask_path = os.path.join(mask_folder, mask_name)
    
    # Prompts en las columnas 4 a 10
    prompts = row[3:10]
    
    # Generar imágenes para cada emoción
    emociones_genericas = ["anger", "fear", "happiness", "neutral", "surprise", "sadness", "disgust"]
    for i, prompt in enumerate(prompts):
        emocion_actual = emociones_genericas[i] if i < len(emociones_genericas) else f"emocion_{i}"
        generate_and_save_inpainting(base_image_path, mask_path, prompt, emocion_actual)
