# hand_detection_service.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import base64

app = Flask(__name__)
detector = HandDetector(detectionCon=0.8, maxHands=2)

@app.route('/detect', methods=['POST'])
def detect():
    try:
        nparr = np.frombuffer(request.data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
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
        return jsonify({'hands': results, 'image': img_str})
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
