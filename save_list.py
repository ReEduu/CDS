import pandas as pd

def store_strings_in_dataframe(df, formatted_reply, emotion):
    # Definir el mapeo de emociones a columnas
    emotion_column_mapping = {
        'sadness': 'sadness',
        'neutral': 'neutral',
        'fear': 'fear',
        'happiness': 'happiness',
        'surprise': 'surprise',
        'anger': 'anger',
        'disgust': 'disgust'
    }
    
    # Verificar la emoción y determinar en qué columna almacenar los strings
    emotion_column = emotion_column_mapping.get(emotion)
    
    if emotion_column is not None:
        df[emotion_column] = formatted_reply
    else:
        print("Emotion not recognized.")
    
    return df

# Crear un DataFrame vacío con 7 columnas y 10 filas
columns = ['sadness', 'neutral', 'fear', 'happiness', 'surprise', 'anger', 'disgust']
initial_df = pd.DataFrame(columns=columns, index=range(10))

# Ejemplo de uso para mantener los datos anteriores
formatted_reply_1 = ['string1', 'string2', 'string3', 'string4', 'string5', 'string6', 'string7', 'string8', 'string9', 'string10']
emotion_1 = 'happiness'
result_df = store_strings_in_dataframe(initial_df.copy(), formatted_reply_1, emotion_1)
print("DataFrame después de la primera llamada:")
print(result_df)

formatted_reply_2 = ['str_a', 'str_b', 'str_c', 'str_d', 'str_e', 'str_f', 'str_g', 'str_h', 'str_i', 'str_j']
emotion_2 = 'sadness'
result_df = store_strings_in_dataframe(result_df.copy(), formatted_reply_2, emotion_2)
print("\nDataFrame después de la segunda llamada:")
print(result_df)
