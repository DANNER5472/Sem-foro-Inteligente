VERDE = "VERDE"
AMARILLO = "AMARILLO"
ROJO = "ROJO"

class ControladorSemaforo:
    def __init__(self):
        self.estado = VERDE
        self.tiempo_verde = 10
        self.tiempo_amarillo = 3
        self.tiempo_rojo = 10
        self.contador_frames = 0
        self.fps = 30

    def ajustar_tiempos(self, vehiculos, peatones):
       

        # Caso 1: Muchos peatones → prioridad peatones
        if peatones > 5:
            self.tiempo_rojo = 20    # más tiempo para que crucen
            self.tiempo_verde = 8    # menos verde para autos

        # Caso 2: Muchos autos y pocos peatones → prioridad autos
        elif vehiculos > 10 and peatones <= 4:
            self.tiempo_verde = 20   # más verde para autos
            self.tiempo_rojo = 8     # menos rojo

        # Caso 3: Muchos autos Y muchos peatones → peatones ganan
        elif vehiculos > 10 and peatones > 5:
            self.tiempo_rojo = 18    # peatones cruzan primero
            self.tiempo_verde = 10   # verde normal después

        # Caso 4: Tráfico moderado
        elif vehiculos > 5:
            self.tiempo_verde = 15
            self.tiempo_rojo = 10

        # Caso 5: Poco tráfico → tiempos normales
        else:
            self.tiempo_verde = 10
            self.tiempo_rojo = 10

    def actualizar(self, vehiculos, peatones):
        self.ajustar_tiempos(vehiculos, peatones)
        self.contador_frames += 1

        frames_verde    = self.tiempo_verde    * self.fps
        frames_amarillo = self.tiempo_amarillo * self.fps
        frames_rojo     = self.tiempo_rojo     * self.fps
        ciclo_total     = frames_verde + frames_amarillo + frames_rojo

        pos = self.contador_frames % ciclo_total

        if pos < frames_verde:
            self.estado = VERDE
        elif pos < frames_verde + frames_amarillo:
            self.estado = AMARILLO
        else:
            self.estado = ROJO

        return self.estado