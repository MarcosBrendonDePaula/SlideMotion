import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import pyautogui

webcam: cv2.VideoCapture = None

def listar_cameras_disponiveis():
    num_cameras = 0
    while True:
        webcam = cv2.VideoCapture(num_cameras)
        if not webcam.isOpened():
            break
        else:
            webcam.release()
            num_cameras += 1
    return num_cameras

def listar_dispositivos_video():
    dispositivos = {}
    for i in range(listar_cameras_disponiveis()):
        dispositivos[i] = cv2.VideoCapture(i).getBackendName()
    return dispositivos

def testar_camera(cam_id):
    webcam = cv2.VideoCapture(cam_id)
    if not webcam.isOpened():
        print(f"Erro ao abrir o dispositivo {cam_id}.")
        return
    else:
        print(f"Dispositivo {cam_id}: {listar_dispositivos_video()[cam_id]} está funcionando corretamente.")

def menu_camera():
    global webcam  # Indica que a variável webcam é global
    dispositivos = listar_dispositivos_video()
    if not dispositivos:
        print("Nenhum dispositivo de vídeo encontrado.")
        return
    print("Dispositivos de vídeo disponíveis:")
    for cam_id, dispositivo in dispositivos.items():
        print(f"{cam_id + 1}. {dispositivo}")
    opcao = int(input("Digite o número do dispositivo que deseja usar: "))
    if opcao >= 1 and opcao <= len(dispositivos):
        webcam = cv2.VideoCapture(opcao - 1)
    else:
        print("Opção inválida.")

# Configurar a captura da webcam
menu_camera()
if webcam is not None:
    webcam.set(cv2.CAP_PROP_FPS, 60)

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

while webcam is not None and webcam.isOpened():
    success, img = webcam.read()
    hands, imgDetected = detector.findHands(img)
    handsStatus = {}
    for hand in hands:
        handsStatus[hand['type']] = detector.fingersUp(hand)
        HandlePos[hand['type']] = hand['center']
    if handsStatus.get("Left") is not None:
        hand = handsStatus.get("Left")
        if sum(hand) == 0:
            mouse_position = MController.position
            screen_width, screen_height = pyautogui.size()
            if HandlePos["Left"]:
                hand_x = HandlePos["Left"][0]
                hand_y = HandlePos["Left"][1]
                new_x = screen_width - hand_x
                new_y = hand_y
                MController.position = (new_x, new_y)
    if handsStatus != estadoAtual and handsStatus.get("Right") is not None:
        hand = handsStatus.get("Right")
        if hand == []:
            pass
        print(["right", hand])
    estadoAtual = handsStatus
    cv2.imshow("n", imgDetected)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if webcam is not None:
    webcam.release()
cv2.destroyAllWindows()
