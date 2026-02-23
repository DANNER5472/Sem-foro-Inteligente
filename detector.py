from ultralytics import YOLO
import cv2

modelo = YOLO('yolov8n.pt')

# 0=persona, 2=auto, 3=moto, 5=bus, 7=camión
CLASES_INTERES = [0, 2, 3, 5, 7]

def detectar(frame):
    resultados = modelo(frame, verbose=False, classes=CLASES_INTERES)[0]

    vehiculos = 0
    peatones = 0

    for det in resultados.boxes:
        clase = int(det.cls[0])
        confianza = float(det.conf[0])

        if confianza < 0.6:
            continue

        if clase == 0:
            peatones += 1
        elif clase in [2, 3, 5, 7]:
            vehiculos += 1

    frame_anotado = resultados.plot(conf=False, labels=False)
    return frame_anotado, vehiculos, peatones