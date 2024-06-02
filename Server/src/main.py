from flask import Flask, request, jsonify
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import base64
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
detector = HandDetector(detectionCon=0.8, maxHands=2)
executor = ThreadPoolExecutor(max_workers=10)  # Define o número máximo de threads

@app.route('/detect', methods=['POST'])
def detect():
    try:
        nparr = np.frombuffer(request.data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Executa o processamento em uma thread
        future = executor.submit(process_image, img)
        result = future.result()
        
        return jsonify(result)
    except Exception as e:
        return str(e), 500

def process_image(img):
    hands, imgDetected = detector.findHands(img)
    handsStatus = {}
    results = []
    for hand in hands:
        handType = hand['type']
        fingers = detector.fingersUp(hand)
        center = hand['center']
        results.append({'type': handType, 'fingers': fingers, 'center': center, 'lmList':hand['lmList']})
    _, buffer = cv2.imencode('.jpg', imgDetected)
    img_str = base64.b64encode(buffer).decode()
    return {'hands': results, 'image': img_str}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
