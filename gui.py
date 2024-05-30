# gui.py
import tkinter as tk
from tkinter import ttk
from hand_detection import start_hand_detection

def list_available_cameras(max_cameras=10):
    import cv2
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(f"Câmera {i}")
            cap.release()
    return available_cameras

def select_camera():
    def on_select(event):
        camera_index = camera_combo.current()
        root.destroy()
        start_hand_detection(camera_index)

    available_cameras = list_available_cameras()

    root = tk.Tk()
    root.title("Seleção de Câmera")

    tk.Label(root, text="Selecione a câmera:").pack(pady=10)

    camera_combo = ttk.Combobox(root, values=available_cameras)
    camera_combo.pack(pady=10)
    if available_cameras:
        camera_combo.current(0)

    camera_combo.bind("<<ComboboxSelected>>", on_select)
    root.mainloop()
