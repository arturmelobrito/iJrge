from ultralytics import YOLO
import cv2
import face_recognition

# Carregar o modelo YOLOv8 pré-treinado para detecção de pessoas
model = YOLO("yolov8n.pt")  # Usa a versão 'nano' (mais leve)


def detect_person_facing(image_path):
    image = cv2.imread(image_path)
    results = model(image)  # Faz a inferência

    persons_detected = 0

    for result in results:
        for box in result.boxes:
            if int(box.cls) == 0:  # Classe 0 = Pessoa
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Recortar a região onde a pessoa foi detectada
                person_region = image[y1:y2, x1:x2]

                # Detectar rostos dentro da pessoa detectada
                face_locations = face_recognition.face_locations(person_region)

                if (
                    face_locations
                ):  # Se um rosto foi encontrado, a pessoa está de frente
                    persons_detected += 1
                    print("✅ Pessoa de frente detectada!")

    if persons_detected > 0:
        return True
    else:
        print("❌ Nenhuma pessoa de frente detectada.")
        return False


# Measure time
import time

start_time = time.time()

detect_person_facing("duas-pessoas-de-lado-meio-de-longe.png")

end_time = time.time()
print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
