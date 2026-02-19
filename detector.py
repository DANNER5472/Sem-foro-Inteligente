from ultralytics import YOLO
import cv2

# Cargamos el modelo YOLOv8 pequeño (se descarga automáticamente la primera vez)
modelo = YOLO('yolov8n.pt')

# Clases que nos interesan detectar
# En YOLO: 0=persona, 2=auto, 3=moto, 5=bus, 7=camión
CLASES_INTERES = [0, 2, 3, 5, 7]

def detectar(frame):
    
    resultados = modelo(frame, verbose=False)[0]

    vehiculos = 0
    peatones = 0

    for det in resultados.boxes:
        clase = int(det.cls[0])
        confianza = float(det.conf[0])

        if confianza < 0.5:  # ignoramos detecciones poco confiables
            continue

        if clase == 0:
            peatones += 1
        elif clase in [2, 3, 5, 7]:
            vehiculos += 1

    # Dibujamos las detecciones en el frame
    frame_anotado = resultados.plot()

    return frame_anotado, vehiculos, peatones