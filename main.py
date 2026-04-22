import cv2
import mediapipe as mp
import time
import tkinter as tk
import os
from PIL import Image, ImageTk, ImageSequence
from pygame import mixer

# --- CONFIGURAÇÕES ---
SENSIBLE = 0.12 
DELAY_AVISO = 1.0 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

class SegurinhoFocus:
    def __init__(self):
        # MediaPipe Pose Otimizado
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(model_complexity=0)
        
        # Inicialização do Áudio
        mixer.init()
        self.sounds = {
            "rock": mixer.Sound(os.path.join(ASSETS, "audios", "the_rock.mp3")),
            "skeleton": mixer.Sound(os.path.join(ASSETS, "audios", "skeleton.mp3"))
        }

        # Estado do Sistema
        self.distraido_desde = None
        self.em_alerta = False

        # Configuração da UI (Tkinter)
        self.root = tk.Tk()
        self.root.withdraw() # Esconde a janela principal
        self.popups = []
        self.criar_janelas_estaticas()

    def criar_janelas_estaticas(self):
        """Cria as janelas uma única vez para evitar travamentos."""
        for nome in ["the_rock", "skeleton"]:
            win = tk.Toplevel(self.root)
            win.withdraw() # Começam escondidas
            win.overrideredirect(True)
            win.attributes("-topmost", True)
            
            w, h = 320, 320
            # Posicionamento fixo (Esquerda e Direita)
            x = (win.winfo_screenwidth() // 2) + (-250 if nome == "the_rock" else 250)
            y = (win.winfo_screenheight() // 2) - 160
            win.geometry(f"{w}x{h}+{x}+{y}")

            # Carrega GIF
            gif_path = os.path.join(ASSETS, "gif", f"{nome}.gif" if nome == "the_rock" else "skeleton_war.gif")
            img = Image.open(gif_path)
            frames = [ImageTk.PhotoImage(f.copy().convert('RGBA').resize((w, h))) for f in ImageSequence.Iterator(img)]
            
            lbl = tk.Label(win, bg="black")
            lbl.pack(expand=True, fill="both")

            def anim(l, fs, i):
                if win.winfo_exists():
                    l.configure(image=fs[i % len(fs)])
                    win.after(80, anim, l, fs, i + 1)
            
            anim(lbl, frames, 0)
            self.popups.append({"win": win, "name": nome})

    def toggle_alertas(self, ativar):
        """Apenas esconde ou mostra, sem destruir nada."""
        if ativar and not self.em_alerta:
            self.em_alerta = True
            for p in self.popups:
                p["win"].deiconify() # Mostra
            self.sounds["rock"].play(loops=-1)
            self.sounds["skeleton"].play(loops=-1)
        elif not ativar and self.em_alerta:
            self.em_alerta = False
            mixer.stop()
            for p in self.popups:
                p["win"].withdraw() # Esconde

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # Resolução leve
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("Segurinho modo Vigilante: Operacional 🛡️")

        while cap.isOpened():
            success, frame = cap.read()
            if not success: break
            
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # Processa Pose
            rgb = cv2.cvtColor(cv2.resize(frame, (320, 240)), cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)

            cor = (0, 255, 0)
            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                # Lógica: Nariz vs Ombros
                dist = (lm[11].y + lm[12].y) / 2 - lm[0].y

                if dist < SENSIBLE:
                    cor = (0, 0, 255)
                    if self.distraido_desde is None:
                        self.distraido_desde = time.time()
                    elif time.time() - self.distraido_desde > DELAY_AVISO:
                        self.toggle_alertas(True)
                else:
                    self.toggle_alertas(False)
                    self.distraido_desde = None

                # Visual Feedback
                nx, ny = int(lm[0].x * w), int(lm[0].y * h)
                cv2.rectangle(frame, (nx-100, ny-100), (nx+100, ny+100), cor, 2)

            cv2.imshow('Segurinho Monitor 🛡️', frame)
            
            # ATENÇÃO: Isso substitui o mainloop e evita travar
            self.root.update() 
            
            if cv2.waitKey(1) & 0xFF == 27: break

        cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    SegurinhoFocus().run()