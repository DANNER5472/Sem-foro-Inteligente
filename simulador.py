import cv2
import numpy as np
from controlador import ControladorSemaforo

# Configuración ventana
ANCHO = 800
ALTO  = 600

def dibujar_semaforo(frame, estado, tiempo_restante):
    # Caja del semáforo
    cv2.rectangle(frame, (50, 50), (150, 350), (40, 40, 40), -1)
    cv2.rectangle(frame, (50, 50), (150, 350), (200, 200, 200), 2)

    # Círculo ROJO
    color_rojo = (0, 0, 255) if estado == "ROJO" else (0, 0, 80)
    cv2.circle(frame, (100, 120), 35, color_rojo, -1)

    # Círculo AMARILLO
    color_amarillo = (0, 255, 255) if estado == "AMARILLO" else (0, 80, 80)
    cv2.circle(frame, (100, 210), 35, color_amarillo, -1)

    # Círculo VERDE
    color_verde = (0, 255, 0) if estado == "VERDE" else (0, 80, 0)
    cv2.circle(frame, (100, 300), 35, color_verde, -1)

    # Tiempo restante
    cv2.putText(frame, f"{tiempo_restante}s", (70, 400),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                (0,255,0) if estado=="VERDE" else (0,0,255) if estado=="ROJO" else (0,255,255), 3)

def dibujar_sliders(frame, vehiculos, peatones):
    # Título
    cv2.putText(frame, "SEMAFORO INTELIGENTE IA", (200, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Slider autos
    cv2.putText(frame, f"Autos: {vehiculos}", (200, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.rectangle(frame, (200, 135), (700, 160), (60, 60, 60), -1)
    ancho_auto = int((vehiculos / 20) * 500)
    cv2.rectangle(frame, (200, 135), (200 + ancho_auto, 160), (100, 100, 255), -1)

    # Slider peatones
    cv2.putText(frame, f"Peatones: {peatones}", (200, 210),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.rectangle(frame, (200, 225), (700, 250), (60, 60, 60), -1)
    ancho_peat = int((peatones / 20) * 500)
    cv2.rectangle(frame, (200, 225), (200 + ancho_peat, 250), (100, 255, 100), -1)

    # Instrucciones
    cv2.putText(frame, "A/Z = autos +/-     P/L = peatones +/-     Q = salir", (150, 560),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

def dibujar_decision(frame, vehiculos, peatones, estado):
    if peatones > 5:
        msg = "PRIORIDAD: PEATONES"
        color = (0, 255, 100)
    elif vehiculos > 10 and peatones <= 4:
        msg = "PRIORIDAD: AUTOS"
        color = (100, 100, 255)
    elif vehiculos > 10 and peatones > 5:
        msg = "CONFLICTO: PEATONES GANAN"
        color = (0, 200, 255)
    elif vehiculos > 5:
        msg = "TRAFICO MODERADO"
        color = (200, 200, 0)
    else:
        msg = "TRAFICO NORMAL"
        color = (200, 200, 200)

    cv2.rectangle(frame, (180, 300), (750, 350), (30, 30, 30), -1)
    cv2.putText(frame, msg, (200, 335),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

# ── Programa principal ──
controlador = ControladorSemaforo()
vehiculos = 3
peatones  = 1

while True:
    frame = np.zeros((ALTO, ANCHO, 3), dtype=np.uint8)

    estado = controlador.actualizar(vehiculos, peatones)

    # Calcular tiempo restante
    fps = controlador.fps
    ciclo = controlador.contador_frames % (
        (controlador.tiempo_verde + controlador.tiempo_amarillo + controlador.tiempo_rojo) * fps
    )
    if estado == "VERDE":
        restante = controlador.tiempo_verde * fps - ciclo
    elif estado == "AMARILLO":
        restante = (controlador.tiempo_verde + controlador.tiempo_amarillo) * fps - ciclo
    else:
        restante = (controlador.tiempo_verde + controlador.tiempo_amarillo + controlador.tiempo_rojo) * fps - ciclo

    segundos = max(0, int(restante / fps))

    dibujar_semaforo(frame, estado, segundos)
    dibujar_sliders(frame, vehiculos, peatones)
    dibujar_decision(frame, vehiculos, peatones, estado)

    cv2.imshow("Simulador Semaforo Inteligente", frame)

    tecla = cv2.waitKey(33) & 0xFF  # ~30 FPS
    if tecla == ord('q'):
        break
    elif tecla == ord('a') and vehiculos < 20:
        vehiculos += 1
    elif tecla == ord('z') and vehiculos > 0:
        vehiculos -= 1
    elif tecla == ord('p') and peatones < 20:
        peatones += 1
    elif tecla == ord('l') and peatones > 0:
        peatones -= 1

cv2.destroyAllWindows()