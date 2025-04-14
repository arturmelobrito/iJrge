import os
import cv2
from services.facial_recognition import *


recognizer = FaceRecognition(recog_threshold=0.5)

def call_facial_recog(image):

    imagem = face_recognition.load_image_file(image)

    face_locations, detected_names = recognizer.recognize_faces(imagem)

    # Desenha os rostos reconhecidos na imagem
    recognized_image = recognizer.draw_recognized_faces(imagem, face_locations, detected_names)

    detected_names = [nome for nome in set(detected_names) if nome != 'Desconhecido']
    detected = len(detected_names) > 0

    return detected, detected_names