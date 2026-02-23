import cv2
import numpy as np
from detector import detectar
from controlador import ControladorSemaforo

COLORES = {
    "VERDE":    (0, 255, 0),
    "AMARILLO": (0, 255, 255),
    "ROJO":     (0, 0, 255)
}

def dibujar_panel(frame, estado, vehiculos, peatones, controlador):
    overlay = frame.copy()

    # Panel de fondo semitransparente
    cv2.rectangle(overlay, (10, 10), (280, 320), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Título
    cv2.putText(frame, "SEMAFORO IA", (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Semáforo visual con círculos
    colores_semaforo = {
        "ROJO":     [(0, 0, 180),    (0, 255, 0),   (0, 255, 255)],
        "AMARILLO": [(0, 0, 100),    (0, 100, 0),   (0, 255, 255)],
        "VERDE":    [(0, 0, 100),    (0, 255, 0),   (0, 100, 100)]
    }

    posiciones = [80, 140, 200]
    nombres    = ["ROJO", "AMARILLO", "VERDE"]
    colores_base = [(0,0,180), (0,180,180), (0,180,0)]
    colores_activos = {
        "ROJO":     (0, 0, 255),
        "VERDE":    (0, 255, 0),
        "AMARILLO": (0, 255, 255)
    }

    for i, (y, nombre, color_base) in enumerate(zip(posiciones, nombres, colores_base)):
        if nombre == estado:
            color = colores_activos[estado]
            radio = 30
        else:
            color = color_base
            radio = 25
        cv2.circle(frame, (60, y), radio, color, -1)
        cv2.circle(frame, (60, y), radio, (255,255,255), 1)

    # Estado en texto
    color_texto = COLORES[estado]
    cv2.putText(frame, estado, (95, 155),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_texto, 3)

    # Línea separadora
    cv2.line(frame, (20, 215), (270, 215), (100, 100, 100), 1)

    # Contadores
    # Contadores más grandes a la derecha
    cv2.rectangle(overlay, (900, 10), (1270, 130), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    cv2.putText(frame, f"Vehiculos: {vehiculos}", (910, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    cv2.putText(frame, f"Peatones:  {peatones}", (910, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # Barra de tiempo restante
    fps = controlador.fps
    if estado == "VERDE":
        total = controlador.tiempo_verde * fps
    elif estado == "AMARILLO":
        total = controlador.tiempo_amarillo * fps
    else:
        total = controlador.tiempo_rojo * fps

    ciclo = controlador.contador_frames % (
        (controlador.tiempo_verde + controlador.tiempo_amarillo + controlador.tiempo_rojo) * fps
    )
    if estado == "VERDE":
        transcurrido = ciclo
    elif estado == "AMARILLO":
        transcurrido = ciclo - controlador.tiempo_verde * fps
    else:
        transcurrido = ciclo - (controlador.tiempo_verde + controlador.tiempo_amarillo) * fps

    restante = max(0, total - transcurrido)
    segundos_restantes = int(restante / fps)

    # Número grande de tiempo restante
    cv2.putText(frame, f"{segundos_restantes}s", (80, 310),
                cv2.FONT_HERSHEY_SIMPLEX, 2.5, COLORES[estado], 4)
    cv2.putText(frame, "restantes", (30, 340),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    return frame

# ── Programa principal ──
cap = cv2.VideoCapture("video/trafico.mp4")
controlador = ControladorSemaforo()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Video terminado")
        break

    frame_anotado, vehiculos, peatones = detectar(frame)
    estado = controlador.actualizar(vehiculos, peatones)
    frame_final = dibujar_panel(frame_anotado, estado, vehiculos, peatones, controlador)
    frame_final = cv2.resize(frame_final, (1600, 900))

    cv2.imshow("Semaforo Inteligente", frame_final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()