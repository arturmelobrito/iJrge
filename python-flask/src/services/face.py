# from ultralytics import YOLO
import cv2
import numpy as np

# model = YOLO("yolov8n.pt")


# def detect_person(image_path):
#     results = model(image_path)

#     for result in results:
#         for box in result.boxes:
#             if int(box.cls) == 0:
#                 print("✅ Pessoa detectada!")
#                 return True

#     print("❌ Nenhuma pessoa detectada.")
#     return False


class FaceDetectionService:
    def __init__(self):
        # Carregar o classificador Haar Cascade para detecção facial

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect_face(self, image_data):
        """
        Detecta se há rostos na imagem fornecida.

        Args:
            image_data (bytes): Dados da imagem em bytes

        Returns:
            dict: Resultado da detecção com contagem de faces e status
        """
        try:
            # Converter bytes da imagem para formato numpy

            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Converter para escala de cinza para detecção
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detectar faces
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            face_count = len(faces)

            return {
                "has_face": face_count > 0,
                "face_count": face_count,
                "status": "success",
            }

        except Exception as e:
            return {
                "has_face": False,
                "face_count": 0,
                "status": "error",
                "message": str(e),
            }


# image_path = "pessoa.jpg"
# detect_person(image_path)
