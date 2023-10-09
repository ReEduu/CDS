import os
import csv
import argparse
import openai
import time

from transformers import pipeline

openai.api_key = "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"


def format_reply(text,  num_elements=10):
    lines = text.strip().split('\n')
    extracted_texts = []

    for line in lines:
        parts = line.split(': ')
        if len(parts) > 1:
            _, extracted_text = parts
            extracted_texts.append(extracted_text)
            
            if len(extracted_texts) >= num_elements:
                break

    return extracted_texts

#Capitulo 1: cambiar redaccion, tiempo
#Capitulo 2: revision del estado del arte
#Capitulo 3: metodologia bien definida, propuesta de solucion. Diagramas, algoritmica, modelos, 
#Capitulo 4: resultados, experimentos, analisis
#Capitulo 5: conclusiones relacionadas a objetivos, hipotesis, comentar partes tecnicas, 
# 3 y 4


def generate_inpainting_prompts(description, emotion):
    prompts = []
    prompt = f"I am going to give you the description of an image and I need you to generate 10 prompts that are suitable for an inpainting model. These prompts should be generated with the goal of intensifying the following emotion in the image for the person viewing it: {emotion}. I also need you to generate prompts on a scale of 1 to 10, where 1 means to intensify the emotion a little and 10 means to intensify the emotion a lot, I need 1 prompt for each level. The inpainting model allows a maximum of 77 tokens so each of your generated prompts should be around that length or a little less. Try to generate prompts with concrete elements that intensify emotions, the inpainting model does not understand abstract things like emotions very well, so avoid generating prompts with adjectives that include emotions. Description: {description}. It is important that your answer must follow the next text format: emotion-level:prompt."
    prompts.append(prompt)
    return prompts

def process_images_and_save_descriptions(mode):
    folder_name = None
    with open("imagenes.csv", "r", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row_number, row in enumerate(csv_reader):
            if row_number == 0:
                folder_name = row[0]
                break  # Salir del bucle después de obtener el nombre de la carpeta

    if folder_name is None:
        print("No se pudo obtener el nombre de la carpeta desde el archivo CSV.")
        return

    # Carpeta de imágenes y modelo de procesamiento
    images_folder = os.path.join(os.getcwd(), "imagenes", folder_name, "imagenes")
    text_to_image = pipeline("image-to-text", model="prasanna2003/blip-image-captioning")

    # Procesar imágenes y generar prompts de inpainting
    if mode == 1:
        with open(os.path.join(os.getcwd(), "descriptions.csv"), "w", newline="") as output_csv:
            csv_writer = csv.writer(output_csv)
            for image_filename in os.listdir(images_folder):
                if image_filename.startswith(".DS_Store"):
                    continue

                image_path = os.path.join(images_folder, image_filename)

                # Procesar imagen
                output = text_to_image(image_path)
                generated_text = output[0]['generated_text']
                start_index = generated_text.index(':') + 2
                end_index = generated_text.index('.')
                format_text = generated_text[start_index:end_index]

                # Escribir en el archivo CSV de descripciones
                csv_writer.writerow([folder_name, image_filename, format_text])

    elif mode == 2:
        if not os.path.exists("descriptions.csv"):
            #print("El archivo 'descriptions.csv' no está generado en el modo 1. Ejecutando modo 1...")
            process_images_and_save_descriptions(1)  # Ejecutar el modo 1 primero

        with open(os.path.join(os.getcwd(), "descriptions.csv"), "r", encoding="utf-8-sig") as input_csv:
            csv_reader = csv.reader(input_csv)
            rows = list(csv_reader)

        prompts_added = 0
        with open(os.path.join(os.getcwd(), "descriptions.csv"), "w", newline="") as output_csv:
            csv_writer = csv.writer(output_csv)
            for row in rows:
                new_row = row.copy()
                description = row[2]  # Descripción de la imagen

                inpainting_prompts = generate_inpainting_prompts(description,"anger")

                lista_column = []

                for i, prompt in enumerate(inpainting_prompts):
                    if len(prompt.split()) <= 700:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are an artist specializing in image inpainting."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=1,
                            max_tokens=77*10,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0
                        )
                        reply = response.choices[0].message.content
                        formatted_reply = format_reply(reply)
                        print(formatted_reply)
                        prompts_added += 1
                        lista_column.extend(formatted_reply)
               
                        if prompts_added % 3 == 0:
                            print("Esperando 1 minuto...")
                            time.sleep(60) 

                new_row += lista_column
                csv_writer.writerow(new_row)

        print(f"Prompts de inpainting generados y agregados: {prompts_added*10}")

def main():
    parser = argparse.ArgumentParser(description="Procesar imágenes y generar prompts para inpainting")
    parser.add_argument("--mode", type=int, choices=[1, 2], default=1, help="Modo: 1 (por defecto) o 2")
    args = parser.parse_args()

    process_images_and_save_descriptions(args.mode)

if __name__ == "__main__":
    main()
