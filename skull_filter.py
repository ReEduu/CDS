import cv2
import mediapipe as mp

# Inicializar el módulo de detección de caras y gestos de Mediapipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Cargar la imagen de la calavera
skull_image = cv2.imread('imagenes/paint/imagenes/paint.jpg')

cap = cv2.VideoCapture(0)  # Iniciar la cámara

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5) as face_mesh:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detección de gestos faciales
        results = face_mesh.process(frame)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark  # Usar el primer rostro detectado
            # Aquí debes mapear los landmarks de la cara a los puntos en la calavera
            # y ajustar la posición de la calavera en función de los landmarks
            
            # Superponer la calavera en el frame
            # (esto es solo un ejemplo, necesitas ajustar la lógica)
            frame[y:y+h, x:x+w] = skull_image
            
        cv2.imshow('Skull Filter', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
