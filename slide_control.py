# slide_control.py
from pynput.keyboard import Key, Controller as KeyboardController

KBController = KeyboardController()

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
