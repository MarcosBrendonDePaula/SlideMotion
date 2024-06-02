pyinstaller --onefile --name client .\main.py
pyinstaller --onefile --name server --add-data ".venv/Lib/site-packages/mediapipe:mediapipe/" .\hand_detection_service.py
