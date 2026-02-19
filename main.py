import cv2
from detector import detectar
from controlador import ControladorSemaforo

# Colores para dibujar el semáforo (en formato BGR de OpenCV)
COLORES = {
    "VERDE":    (0, 255, 0),
    "AMARILLO": (0, 255, 255),
    "ROJO":     (0, 0, 255)
}

def dibujar_semaforo(frame, estado, vehiculos, peatones):
    """
    Dibuja en pantalla el estado del semáforo y los conteos
    """
    color = COLORES[estado]

    # Rectángulo de fondo
    cv2.rectangle(frame, (10, 10), (300, 120), (0, 0, 0), -1)

    # Texto del estado
    cv2.putText(frame, f"Semaforo: {estado}", (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Conteo de vehículos y peatones
    cv2.putText(frame, f"Vehiculos: {vehiculos}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Peatones: {peatones}", (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return frame

# ── Programa principal ──
cap = cv2.VideoCapture("video/trafico.mp4")
controlador = ControladorSemaforo()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Video terminado")
        break

    # Detectamos con YOLO
    frame_anotado, vehiculos, peatones = detectar(frame)

    # Actualizamos el semáforo
    estado = controlador.actualizar(vehiculos, peatones)

    # Dibujamos info en pantalla
    frame_final = dibujar_semaforo(frame_anotado, estado, vehiculos, peatones)

    # Mostramos el video
    frame_final = cv2.resize(frame_final, (1280, 720))
    cv2.imshow("Semaforo Inteligente", frame_final)

    # Presiona Q para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()