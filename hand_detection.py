# hand_detection.py
import cv2
import numpy as np
import pyautogui
import requests
import base64
import json
from utils import calculate_distance, smooth_move
from slide_control import pass_slide
from pynput.mouse import Controller as MouseController

MController = MouseController()

def process_hand_movement(handsStatus, HandlePos):
    if handsStatus.get("Left") is not None:
        hand = handsStatus.get("Left")
        if sum(hand) == 0:
            mouse_position = MController.position  # Obtém a posição atual do mouse
            screen_width, screen_height = pyautogui.size()  # Obtém as dimensões da tela
            if HandlePos["Left"]:
                hand_x = HandlePos["Left"][0]
                hand_y = HandlePos["Left"][1]
                new_mouse_position = smooth_move(mouse_position, (hand_x * screen_width, hand_y * screen_height))
                MController.position = new_mouse_position

def start_hand_detection(camera_index):
    webcam = cv2.VideoCapture(camera_index)
    slideState = {"Right": 'not_sliding', "Left": 'not_sliding'}
    handsStatus = {}
    HandlePos = {}

    while webcam.isOpened():
        success, img = webcam.read()
        if not success:
            break

        _, img_encoded = cv2.imencode('.jpg', img)
        response = requests.post('http://127.0.0.1:5000/detect', data=img_encoded.tobytes())
        response_data = response.json()

        hands = response_data['hands']
        img_str = response_data['image']
        img_decoded = base64.b64decode(img_str)
        img_detected = cv2.imdecode(np.frombuffer(img_decoded, np.uint8), -1)

        for hand in hands:
            handType = hand['type']
            handsStatus[handType] = hand['fingers']
            HandlePos[handType] = hand['center']

            if handType in ["Right", "Left"]:
                thumb_tip = hand['lmList'][4][:2]  # Ponto 4 é a ponta do polegar
                index_tip = hand['lmList'][8][:2]  # Ponto 8 é a ponta do indicador
                distance = calculate_distance(thumb_tip, index_tip)
                # Passar slide se o polegar e o indicador se aproximarem
                pass_slide(handType, distance, slideState=slideState)

        process_hand_movement(handsStatus, HandlePos)
        cv2.imshow("Hand Detection", img_detected)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty("Hand Detection", cv2.WND_PROP_VISIBLE) < 1:
            break

    webcam.release()
    cv2.destroyAllWindows()