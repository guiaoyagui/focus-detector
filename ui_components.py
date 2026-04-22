import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from pygame import mixer
import random
import threading

def disparar_alerta(tipo, caminhos):
    """
    Função auxiliar para rodar o popup em uma thread separada,
    evitando que o Tkinter trave o processamento da câmera.
    """
    thread = threading.Thread(target=mostrar_popup_distracao, args=(tipo, caminhos))
    thread.daemon = True
    thread.start()

def mostrar_popup_distracao(tipo, caminhos):
    """
    Cria a janela pop-up com o GIF e o áudio correspondente.
    """
    root = tk.Tk()
    root.title("⚠️ FOCO TOTAL! ⚠️")
    
    # Configurações de Janela "Always on Top" e sem bordas (opcional)
    root.attributes("-topmost", True)
    # root.overrideredirect(True) # Ative se quiser esconder os botões de fechar

    # Sorteia uma posição aleatória na tela para o susto ser maior
    largura, altura = 400, 400
    pos_x = random.randint(0, root.winfo_screenwidth() - largura)
    pos_y = random.randint(0, root.winfo_screenheight() - altura)
    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # --- Gerenciamento de Áudio ---
    if not mixer.get_init():
        mixer.init()
    
    mixer.music.load(caminhos[tipo]["audio"])
    mixer.music.play()

    # --- Gerenciamento do GIF ---
    img_path = caminhos[tipo]["gif"]
    img = Image.open(img_path)
    
    # Prepara os frames do GIF
    frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA').resize((400, 400))) 
              for frame in ImageSequence.Iterator(img)]
    
    label = tk.Label(root, bg='black')
    label.pack(expand=True, fill='both')

    def animate(frame_idx):
        frame = frames[frame_idx]
        label.configure(image=frame)
        root.after(50, animate, (frame_idx + 1) % len(frames))

    # Inicia a animação
    animate(0)

    # Fecha a janela automaticamente após 4 segundos para você voltar ao trabalho
    root.after(4000, root.destroy)
    
    root.mainloop()