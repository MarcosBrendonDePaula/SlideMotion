import math
import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import pyautogui
import tkinter as tk
from tkinter import ttk

# Inicializar o controlador de teclado e mouse
KBController = KeyboardController()
MController = MouseController()

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def pass_slide(handType, distance, slideState, threshold=50):
    if distance < threshold:
        if slideState.get(handType) == 'not_sliding':
            if handType == "Right":
                KBController.press(Key.right)
                KBController.release(Key.right)
                print("Slide para a direita")
            elif handType == "Left":
                KBController.press(Key.left)
                KBController.release(Key.left)
                print("Slide para a esquerda")
            slideState[handType] = 'sliding'
    else:
        slideState[handType] = 'not_sliding'

def smooth_move(current_pos, target_pos, smoothing_factor=0.2, min_move_threshold=5):
    new_x = current_pos[0] + (target_pos[0] - current_pos[0]) * smoothing_factor
    new_y = current_pos[1] + (target_pos[1] - current_pos[1]) * smoothing_factor
    if abs(new_x - current_pos[0]) < min_move_threshold and abs(new_y - current_pos[1]) < min_move_threshold:
        return current_pos  # Retorna a posição atual se o movimento for menor que o limiar
    return new_x, new_y

def process_hand_movement(handsStatus, HandlePos):
    if handsStatus.get("Left") is not None:
        hand = handsStatus.get("Left")
        if sum(hand) == 0:
            mouse_position = MController.position  # Obtém a posição atual do mouse
            screen_width, screen_height = pyautogui.size()  # Obtém as dimensões da tela
            if HandlePos["Left"]:
                hand_x = HandlePos["Left"][0]
                hand_y = HandlePos["Left"][1]
                target_x = screen_width - hand_x  # Inverte a posição X da mão em relação à tela
                target_y = hand_y  # Mantém a posição Y da mão
                smooth_x, smooth_y = smooth_move(mouse_position, (target_x, target_y))  # Movimento suave

                if (smooth_x, smooth_y) != mouse_position:  # Atualizar posição apenas se houver movimento significativo
                    MController.position = (smooth_x, smooth_y)  # Define a nova posição do mouse

def start_hand_detection(camera_index):
    # Configurar a captura da webcam
    webcam = cv2.VideoCapture(camera_index)  # Selecionar a câmera com base no índice
    webcam.set(cv2.CAP_PROP_FPS, 60)  # Limitar a taxa de quadros da webcam para 60 FPS

    # Inicializar o detector de mãos
    detector = HandDetector(detectionCon=0.9)
    estadoAtual = {
        'left': [0, 0, 0, 0, 0],
        'right': [0, 0, 0, 0, 0]
    }

    HandlePos = {
        'left': [],
        'right': []
    }

    slideState = {
        'left': 'not_sliding',
        'right': 'not_sliding'
    }

    while webcam.isOpened():
        success, img = webcam.read()
        if not success:
            continue

        hands, imgDetected = detector.findHands(img)
        handsStatus = {}
        for hand in hands:
            handType = hand['type']
            handsStatus[handType] = detector.fingersUp(hand)
            HandlePos[handType] = hand['center']

            # Calcular a distância entre o indicador e o polegar
            if handType in ["Right", "Left"]:
                thumb_tip = hand['lmList'][4][:2]  # Ponto 4 é a ponta do polegar
                index_tip = hand['lmList'][8][:2]  # Ponto 8 é a ponta do indicador
                distance = calculate_distance(thumb_tip, index_tip)

                # Passar slide se o polegar e o indicador se aproximarem
                pass_slide(handType, distance, slideState=slideState)

        process_hand_movement(handsStatus, HandlePos)

        estadoAtual = handsStatus
        cv2.imshow("Hand Detection", imgDetected)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Sai do loop se a tecla 'q' for pressionada
            break
        if cv2.getWindowProperty("Hand Detection", cv2.WND_PROP_VISIBLE) < 1:  # Verifica se a janela foi fechada
            break

    webcam.release()
    cv2.destroyAllWindows()

def list_available_cameras(max_cameras=10):
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
        camera_combo.current(0)  # Selecionar a primeira câmera disponível por padrão

    camera_combo.bind("<<ComboboxSelected>>", on_select)
    root.mainloop()

if __name__ == "__main__":
    select_camera()
