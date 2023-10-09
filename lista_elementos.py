import csv

import pandas as pd
import random

def seleccionar_elemento_al_azar(diccionario):
    
    if not diccionario:
        return None, None, None
    
    llave_aleatoria = random.choice(list(diccionario.keys()))
    elemento = diccionario[llave_aleatoria]
    valor = elemento['value']
    
    elemento['count'] += 1
    
    return llave_aleatoria, valor, elemento['count']




def construir_diccionario_desde_csv(archivo_csv):
    elements = {}
    columns = ['sadness', 'neutral', 'fear', 'happiness', 'surprise', 'anger', 'disgust']
    initial_df = pd.DataFrame(columns=columns, index=range(10))

    with open(archivo_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for row in csv_reader:
            if len(row) == 0:
                break
            
            if len(row) >= 3:
                key = row[1]
                value = row[2]
                elements[key] = {'value': value, 'count': 1,'dataframe': initial_df.copy()}
    
    return elements

archivo_csv = 'csv/descriptions.csv'
diccionario = construir_diccionario_desde_csv(archivo_csv)

print(seleccionar_elemento_al_azar(diccionario))
