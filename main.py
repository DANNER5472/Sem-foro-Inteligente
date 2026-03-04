import cv2
import numpy as np
from detector import detectar
from controlador import ControladorSemaforo

COLORES = {
    "VERDE":    (0, 255, 0),
    "AMARILLO": (0, 255, 255),
    "ROJO":     (0, 0, 255)
}

ICONOS_ESTADO = {
    "VERDE":    ">> CIRCULAR",
    "AMARILLO": "!! PRECAUCION",
    "ROJO":     "|| DETENIDO"
}


def dibujar_panel(frame, estado, vehiculos, peatones, controlador):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    # ── Panel izquierdo: semáforo ──────────────────────────────────────
    cv2.rectangle(overlay, (10, 10), (210, 460), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    cv2.putText(frame, "SEMAFORO IA", (20, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.line(frame, (20, 52), (200, 52), (80, 80, 80), 1)

    # Caja del semáforo
    cv2.rectangle(frame, (75, 65), (145, 340), (40, 40, 40), -1)
    cv2.rectangle(frame, (75, 65), (145, 340), (120, 120, 120), 2)

    luces = [
        ("ROJO",     130, (0, 0, 255),     (0, 0, 70)),
        ("AMARILLO", 200, (0, 230, 230),   (0, 70, 70)),
        ("VERDE",    270, (0, 255, 0),     (0, 70, 0)),
    ]

    for nombre, cy, color_activo, color_apagado in luces:
        if nombre == estado:
            color = color_activo
            radio = 30
            # Halo de brillo
            cv2.circle(frame, (110, cy), radio + 6, (*color_activo[:2], color_activo[2] // 3), -1)
        else:
            color = color_apagado
            radio = 24
        cv2.circle(frame, (110, cy), radio, color, -1)
        cv2.circle(frame, (110, cy), radio, (180, 180, 180), 1)

    # Tiempo restante grande
    segundos = controlador.segundos_restantes()
    cv2.putText(frame, f"{segundos}s", (60, 390),
                cv2.FONT_HERSHEY_SIMPLEX, 2.5, COLORES[estado], 5)
    cv2.putText(frame, "restantes", (45, 420),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (160, 160, 160), 1)

    # Ícono de estado
    cv2.putText(frame, ICONOS_ESTADO[estado], (18, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLORES[estado], 2)

    # ── Panel superior derecho: contadores ────────────────────────────
    overlay2 = frame.copy()
    panel_x = w - 430
    cv2.rectangle(overlay2, (panel_x, 10), (w - 10, 160), (20, 20, 20), -1)
    cv2.addWeighted(overlay2, 0.7, frame, 0.3, 0, frame)

    # Íconos y contadores
    cv2.putText(frame, f"[AUTO]  Vehiculos: {vehiculos}",
                (panel_x + 10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (100, 180, 255), 2)
    cv2.putText(frame, f"[PEAT]  Peatones:  {peatones}",
                (panel_x + 10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (100, 255, 150), 2)

    # Razón de decisión del ciclo actual
    cv2.putText(frame, f"Motivo: {controlador.razon}",
                (panel_x + 10, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 100), 1)

    # ── Panel de decisión: próximo ciclo ──────────────────────────────
    overlay3 = frame.copy()
    cv2.rectangle(overlay3, (panel_x, 170), (w - 10, 240), (15, 15, 30), -1)
    cv2.addWeighted(overlay3, 0.7, frame, 0.3, 0, frame)

    prox_v, prox_r, prox_razon = controlador.preview_tiempos()
    cv2.putText(frame, "SIGUIENTE CICLO:",
                (panel_x + 10, 195), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)
    cv2.putText(frame,
                f"Verde: {prox_v}s   Rojo: {prox_r}s   |  {prox_razon}",
                (panel_x + 10, 228), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (150, 220, 150), 1)

    # ── Barra de progreso del ciclo ────────────────────────────────────
    fps          = controlador.fps
    tv           = controlador.tiempo_verde    * fps
    ta           = controlador.tiempo_amarillo * fps
    tr           = controlador.tiempo_rojo     * fps
    total_frames = tv + ta + tr
    pos          = controlador.frames_en_ciclo

    bx1, bx2 = 220, w - 20
    by        = h - 45
    bh        = 20
    bw        = bx2 - bx1

    # Fondo
    cv2.rectangle(frame, (bx1, by), (bx2, by + bh), (40, 40, 40), -1)

    # Segmento verde
    x_v = bx1 + int(tv / total_frames * bw)
    cv2.rectangle(frame, (bx1, by), (x_v, by + bh), (0, 140, 0), -1)
    # Segmento amarillo
    x_a = x_v + int(ta / total_frames * bw)
    cv2.rectangle(frame, (x_v, by), (x_a, by + bh), (0, 180, 180), -1)
    # Segmento rojo
    cv2.rectangle(frame, (x_a, by), (bx2, by + bh), (0, 0, 160), -1)

    # Borde
    cv2.rectangle(frame, (bx1, by), (bx2, by + bh), (120, 120, 120), 1)

    # Cursor de posición actual
    if total_frames > 0:
        cursor_x = bx1 + int(min(pos, total_frames) / total_frames * bw)
        cv2.rectangle(frame, (cursor_x - 2, by - 5),
                      (cursor_x + 2, by + bh + 5), (255, 255, 255), -1)

    cv2.putText(frame, "Progreso del ciclo:",
                (bx1, by - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
    cv2.putText(frame, f"Verde={controlador.tiempo_verde}s  Amarillo={controlador.tiempo_amarillo}s  Rojo={controlador.tiempo_rojo}s",
                (bx1 + 280, by - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 160, 160), 1)

    return frame


# ── Programa principal ────────────────────────────────────────────────
cap         = cv2.VideoCapture("video/trafico.mp4")
controlador = ControladorSemaforo()

while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] Video terminado — reiniciando...")
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    frame_anotado, vehiculos, peatones = detectar(frame)
    estado      = controlador.actualizar(vehiculos, peatones)
    frame_final = dibujar_panel(frame_anotado, estado, vehiculos, peatones, controlador)
    frame_final = cv2.resize(frame_final, (1280, 720))

    cv2.imshow("Semaforo Inteligente IA", frame_final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()