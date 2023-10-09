import csv

def guardar_diccionario_a_csv(diccionario, csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['State', 'Total time', 'Transitions'])
        for emocion, info in diccionario.items():
            tiempo_mantenido = info['tiempo_mantenido']
            transiciones = info['transiciones']
            transiciones_str = ', '.join([str(t) for t in transiciones])
            csv_writer.writerow([emocion, tiempo_mantenido, transiciones_str])

    print(f'Se ha guardado el diccionario en el archivo CSV: {csv_file}')

def reconstruir_diccionario_desde_csv(csv_file):
    reconstructed_data = {}

    with open(csv_file, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        for row in csv_reader:
            emocion, tiempo_mantenido, transiciones_str = row
            transiciones = eval(transiciones_str)
            reconstructed_data[emocion] = {
                'total time': float(tiempo_mantenido),
                'transitions': transiciones
            }

    return reconstructed_data

# Ejemplo de uso:
data = {
    'initial_state': {'tiempo_mantenido': 4.48, 'transiciones': [([('husky', 'happiness')], 'happiness', 4.48, 0)]}
}

csv_file = 'datos.csv'
guardar_diccionario_a_csv(data, csv_file)

# Reconstruir el diccionario desde el CSV
diccionario_reconstruido = reconstruir_diccionario_desde_csv(csv_file)
print('Diccionario reconstruido:')
print(diccionario_reconstruido)
