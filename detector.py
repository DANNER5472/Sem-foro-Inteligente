from ultralytics import YOLO
import cv2

modelo = YOLO('yolov8n.pt')

# 0=persona, 2=auto, 3=moto, 5=bus, 7=camión
CLASES_INTERES = [0, 2, 3, 5, 7]

# ── Umbrales ajustados para escenas densas con oclusión ───────────────
CONFIANZA_VEHICULOS = 0.25   # bajo para no perder autos tapados parcialmente
CONFIANZA_PEATONES  = 0.40   # un poco más alto para evitar falsos positivos
IOU_THRESHOLD       = 0.40   # NMS más permisivo → no elimina autos solapados


def detectar(frame):
    resultados = modelo(
        frame,
        verbose=False,
        classes=CLASES_INTERES,
        conf=CONFIANZA_VEHICULOS,   # umbral mínimo global
        iou=IOU_THRESHOLD           # NMS permisivo para escenas densas
    )[0]

    vehiculos = 0
    peatones  = 0

    for det in resultados.boxes:
        clase     = int(det.cls[0])
        confianza = float(det.conf[0])

        if clase == 0:
            # Peatones requieren mayor confianza para evitar falsos positivos
            if confianza >= CONFIANZA_PEATONES:
                peatones += 1
        elif clase in [2, 3, 5, 7]:
            # Vehículos con umbral bajo para capturar los parcialmente ocultos
            if confianza >= CONFIANZA_VEHICULOS:
                vehiculos += 1

    # Dibujar detecciones con confianza visible para debug
    frame_anotado = resultados.plot(conf=True, labels=True)
    return frame_anotado, vehiculos, peatones