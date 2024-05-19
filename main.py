import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import pyautogui

# Configurar a captura da webcam
webcam = cv2.VideoCapture(3)  # Altere para 0 se a webcam for a primeira, 1 se for a segunda, etc.
webcam.set(cv2.CAP_PROP_FPS, 60)  # Limitar a taxa de quadros da webcam para 60 FPS

KBController = KeyboardController()
MController = MouseController()

detector = HandDetector(detectionCon=0.9)
estadoAtual = {
    'left': [0, 0, 0, 0, 0],
    'right': [0, 0, 0, 0, 0]
}

HandlePos = {
    'left': [],
    'right': []
}

while webcam.isOpened():
    success, img = webcam.read()
    hands, imgDetected = detector.findHands(img)
    handsStatus = {}
    for hand in hands:
        handsStatus[hand['type']] = detector.fingersUp(hand)
        HandlePos[hand['type']] = hand['center']
    if handsStatus.get("Left") != None:
        hand = handsStatus.get("Left")
        if sum(hand) == 0:
            mouse_position = MController.position  # Obtém a posição atual do mouse
            screen_width, screen_height = pyautogui.size()  # Obtém as dimensões da tela
            if HandlePos["Left"]:
                hand_x = HandlePos["Left"][0]
                hand_y = HandlePos["Left"][1]
                new_x = screen_width - hand_x  # Inverte a posição X da mão em relação à tela
                new_y = hand_y  # Mantém a posição Y da mão
                MController.position = (new_x, new_y)  # Define a nova posição do mouse
    if handsStatus != estadoAtual and handsStatus.get("Right") != None:
        hand = handsStatus.get("Right")
        if hand == []:
            pass
        print(["right",hand])
    estadoAtual = handsStatus
    cv2.imshow("n", imgDetected)
