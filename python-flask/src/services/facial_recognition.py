import cv2
import numpy as np
import face_recognition
import os
import json

THRESHOLD = 0.5

class FaceRecognition():

    def __init__(self, faces_images_path = "src/user/images/", registers_path = "src/user/registers/", recog_threshold=THRESHOLD):
        
        self.recog_threshold = recog_threshold
        self.faces_images_path = faces_images_path
        self.registers_path = registers_path
        
        self._init_register_faces()
        self._load_registered_faces()
        print("Recognition threshold defined as:", self.recog_threshold)
        
    def _init_register_faces(self):
        """
        Percorre o diretório src/user/images e, para cada arquivo .jpg,
        processa o rosto e salva um arquivo JSON em src/user/registers com o nome da pessoa e o embedding.
        """
        faces_dir = self.faces_images_path
        register_dir = self.registers_path
        
        # Cria o diretório de registros se não existir.
        os.makedirs(register_dir, exist_ok=True)
        
        # Lista os subdiretórios em src/faces/ — cada um representa um usuário.
        for user_dir in os.listdir(faces_dir):
            user_path = os.path.join(faces_dir, user_dir)
            if os.path.isdir(user_path):
                embeddings_list = []
                
                # Processa cada arquivo de imagem dentro do diretório do usuário
                for file in os.listdir(user_path):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file_path = os.path.join(user_path, file)
                        
                        # Carrega a imagem e extrai o embedding do rosto detectado
                        image = face_recognition.load_image_file(file_path)
                        face_encodings = face_recognition.face_encodings(image)
                        
                        if not face_encodings:
                            print(f"[AVISO] Nenhum rosto encontrado em {file_path}, ignorando esta imagem.")
                            continue
                        elif len(face_encodings) > 1:
                            print(f"[AVISO] Mais de um rosto encontrado em {file_path}, ignorando esta imagem.")
                        
                        # Se houver mais de um rosto, utiliza o primeiro embedding
                        embeddings_list.append(face_encodings[0].tolist())
                
                # Se foi possível extrair embeddings de ao menos uma imagem, registra o usuário
                if embeddings_list:
                    data = {
                        "name": user_dir,
                        "embeddings": embeddings_list
                    }
                    register_file = os.path.join(register_dir, f"{user_dir}.json")
                    with open(register_file, "w") as f:
                        json.dump(data, f)
                    print(f"[INFO] Cadastro realizado para '{user_dir}' com {len(embeddings_list)} imagem(ns).")
                else:
                    print(f"[AVISO] Nenhum embedding válido obtido para '{user_dir}'; cadastro ignorado.")

    def _load_registered_faces(self):
        """
        Percorre o diretório src/user/registers/ e carrega os arquivos JSON com os registros dos rostos.
        Retorna um json com os nomes e os embeddings.
        """
        register_dir = self.registers_path
        self.registered_faces = {}

        for filename in os.listdir(register_dir):
            if filename.lower().endswith(".json"):
                file_path = os.path.join(register_dir, filename)

                with open(file_path, "r") as f:
                    data = json.load(f)
                    name = data.get("name")
                    embedding = data.get("embeddings")
                    if name and embedding:
                        self.registered_faces[name] = embedding
                    else:
                        print(f"[AVISO] O arquivo {filename} não possui os dados esperados.")
                        
        print(f"[INFO] Registros carregados: {len(self.registered_faces)} rostos registrados.")
    
    def recognize_faces(self, image):
        """
        Recebe uma imagem (array NumPy, por exemplo, lido pelo OpenCV) e retorna:
        - os locais dos rostos detectados,
        - uma lista com os nomes identificados para cada rosto,
        com base no atributo registered_faces.
        """

        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        detected_names = []
        
        for cod_face in face_encodings:
            recognized_name = "Desconhecido"
            best_distance = None
            best_match_name = None

            for name, embeddings_list in self.registered_faces.items():
                # Para cada embedding cadastrado, calcula a distância
                distances = [
                    np.linalg.norm(np.array(registered_embedding) - cod_face)
                    for registered_embedding in embeddings_list
                ]
                # Seleciona a menor distância entre as imagens desse cadastro
                if distances:
                    min_distance = min(distances)
                    if (best_distance is None) or (min_distance < best_distance):
                        best_distance = min_distance
                        best_match_name = name
            
            # Se a menor distância for inferior ao limiar, considera o rosto reconhecido
            if best_distance is not None and best_distance < self.recog_threshold:
                recognized_name = best_match_name
            
            detected_names.append(recognized_name)
        
        return face_locations, detected_names

    def draw_recognized_faces(self, imagem, locais_dos_rostos, nomes_detectados):
        """
        Desenha retângulos ao redor dos rostos detectados e coloca o nome identificado acima de cada rosto.
        """
        for (top, right, bottom, left), name in zip(locais_dos_rostos, nomes_detectados):
            # Desenha um retângulo ao redor do rosto
            cv2.rectangle(imagem, (left, top), (right, bottom), (0, 255, 0), 2)
            # Coloca o nome acima do rosto
            cv2.putText(imagem, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        
        return cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
