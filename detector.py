import cv2
import mediapipe as mp
import numpy as np

class FocusDetector:
    def __init__(self):
        # Inicializa o MediaPipe Face Mesh (Versão 0.10.33 recomendada)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def estimar_inclinacao(self, frame):
        """
        Processa o frame e retorna o ângulo de inclinação (Pitch).
        Retorna None se nenhum rosto for detectado.
        """
        img_h, img_w, _ = frame.shape
        results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if not results.multi_face_landmarks:
            return None

        face_landmarks = results.multi_face_landmarks[0]
        
        # Pontos 3D de referência (Modelo genérico de rosto)
        # 1: Ponta do nariz, 152: Queixo, 33: Olho esquerdo, 263: Olho direito, 
        # 61: Canto esquerdo boca, 291: Canto direito boca
        face_3d = []
        face_2d = []

        for idx, lm in enumerate(face_landmarks.landmark):
            if idx in [1, 152, 33, 263, 61, 291]:
                x, y = int(lm.x * img_w), int(lm.y * img_h)
                face_2d.append([x, y])
                face_3d.append([x, y, lm.z])

        face_2d = np.array(face_2d, dtype=np.float64)
        face_3d = np.array(face_3d, dtype=np.float64)

        # Configuração da Câmera (Matriz intrínseca aproximada)
        focal_length = 1 * img_w
        cam_matrix = np.array([[focal_length, 0, img_h / 2],
                              [0, focal_length, img_w / 2],
                              [0, 0, 1]])
        
        # Matriz de distorção (assumindo zero para webcams comuns)
        dist_matrix = np.zeros((4, 1), dtype=np.float64)

        # Resolve o problema de PnP (Perspective-n-Point)
        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

        # Converte vetor de rotação em matriz e depois em ângulos de Euler
        rmat, _ = cv2.Rodrigues(rot_vec)
        angles, _, _, _, _, _ = cv2.RQDecomposition(rmat)

        # O Pitch é o ângulo X (inclinação vertical)
        pitch = angles[0] * 360
        
        return pitch