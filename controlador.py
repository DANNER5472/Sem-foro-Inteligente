# Estados posibles del semáforo
VERDE = "VERDE"
AMARILLO = "AMARILLO"
ROJO = "ROJO"

class ControladorSemaforo:
    def __init__(self):
        self.estado = VERDE
        self.tiempo_verde = 10      # segundos base para verde
        self.tiempo_amarillo = 3    # siempre 3 segundos
        self.tiempo_rojo = 10       # segundos base para rojo
        self.contador_frames = 0
        self.fps = 30               # frames por segundo del video

    def ajustar_tiempos(self, vehiculos, peatones):
        """
        La IA decide cuánto tiempo dar según el tráfico detectado
        """
        # Si hay muchos vehículos, más tiempo verde para autos
        if vehiculos > 10:
            self.tiempo_verde = 20
            self.tiempo_rojo = 8
        elif vehiculos > 5:
            self.tiempo_verde = 15
            self.tiempo_rojo = 10
        else:
            self.tiempo_verde = 10
            self.tiempo_rojo = 10

        # Si hay muchos peatones, aumentamos el tiempo rojo (peatones cruzan)
        if peatones > 5:
            self.tiempo_rojo += 5

    def actualizar(self, vehiculos, peatones):
        """
        Avanza el semáforo frame a frame
        """
        self.ajustar_tiempos(vehiculos, peatones)
        self.contador_frames += 1

        # Calculamos cuántos frames dura cada estado
        frames_verde    = self.tiempo_verde    * self.fps
        frames_amarillo = self.tiempo_amarillo * self.fps
        frames_rojo     = self.tiempo_rojo     * self.fps
        ciclo_total     = frames_verde + frames_amarillo + frames_rojo

        # Posición dentro del ciclo actual
        pos = self.contador_frames % ciclo_total

        if pos < frames_verde:
            self.estado = VERDE
        elif pos < frames_verde + frames_amarillo:
            self.estado = AMARILLO
        else:
            self.estado = ROJO

        return self.estado