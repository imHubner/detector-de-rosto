import tkinter as tk
from tkinter import messagebox, Label
from PIL import Image, ImageTk
import cv2
from cvzone.FaceDetectionModule import FaceDetector

# Variável global para armazenar o caminho da captura do rosto
face_image_path = ""

# Função para capturar e salvar o rosto detectado
def login_action():
    global face_image_path
    video = cv2.VideoCapture(0)
    detector = FaceDetector()

    while True:
        _, img = video.read()  # Ler frame da câmera
        img, bboxes = detector.findFaces(img, draw=True)  # Detectar rostos

        # Se um rosto for detectado
        if bboxes:
            confidence = bboxes[0]["score"][0]  # Pegar a confiança da detecção
            if confidence > 0.97:  # Se a confiança for maior que 97%
                face_image_path = "face_detected.png"
                cv2.imwrite(face_image_path, img)  # Salvar a imagem do rosto
                video.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Login", "Login feito com sucesso!")
                show_detected_faces()  # Chamar função para exibir a próxima janela
                break
        
        # Mostrar vídeo em tempo real
        cv2.imshow('Resultado', img)
        
        # Fechar com ESC
        if cv2.waitKey(1) == 27:
            break

    video.release()
    cv2.destroyAllWindows()

# Função para exibir janela com a opção de rostos detectados
def show_detected_faces():
    # Limpar a janela atual
    for widget in root.winfo_children():
        widget.destroy()

    # Carregar a imagem do rosto detectado
    img = Image.open(face_image_path)
    img = img.resize((200, 200))  # Redimensionar para caber na janela
    img_tk = ImageTk.PhotoImage(img)

    # Label para mostrar a imagem
    label = Label(root, image=img_tk)
    label.image = img_tk  # Manter referência da imagem
    label.pack(pady=20)

    # Texto de indicação
    tk.Label(root, text="Rostos Detectados", font=("Arial", 16)).pack(pady=10)

# Criação da interface gráfica com Tkinter
root = tk.Tk()
root.title("Menu Principal")
root.geometry("400x400")

# Criação do botão de Login
login_button = tk.Button(root, text="Login", command=login_action, width=15, height=2)
login_button.pack(pady=150)

# Iniciar loop principal do Tkinter
root.mainloop()
