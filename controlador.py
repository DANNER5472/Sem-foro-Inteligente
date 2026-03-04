VERDE    = "VERDE"
AMARILLO = "AMARILLO"
ROJO     = "ROJO"

# ── Umbrales configurables ─────────────────────────────────────────────
UMBRAL_AUTOS_BAJO  = 5    # < 5 autos  → tiempo normal
UMBRAL_AUTOS_ALTO  = 15   # > 15 autos → tiempo extendido dinámico
SEGUNDOS_POR_AUTO  = 2    # segundos extra por cada auto sobre el umbral alto

TIEMPO_VERDE_NORMAL   = 5    # poco tráfico
TIEMPO_VERDE_MODERADO = 10   # tráfico moderado (5–15 autos)
TIEMPO_VERDE_BASE     = 5    # base para tráfico alto (se suman 2s por auto extra)
TIEMPO_VERDE_MAXIMO   = 60   # techo absoluto de verde

TIEMPO_AMARILLO       = 3    # siempre fijo
TIEMPO_ROJO_NORMAL    = 5    # rojo estándar
TIEMPO_ROJO_PEATONES  = 20   # rojo largo cuando hay peatones


class ControladorSemaforo:
    def __init__(self):
        self.estado          = ROJO
        self.fps             = 30

        # Tiempos del ciclo ACTUAL — no cambian hasta que el ciclo termine
        self.tiempo_verde    = TIEMPO_VERDE_NORMAL
        self.tiempo_amarillo = TIEMPO_AMARILLO
        self.tiempo_rojo     = TIEMPO_ROJO_NORMAL

        # Tiempos pendientes — se aplican al inicio del SIGUIENTE ciclo
        self._prox_verde     = TIEMPO_VERDE_NORMAL
        self._prox_rojo      = TIEMPO_ROJO_NORMAL
        self._prox_razon     = "Trafico normal"

        # Razón del ciclo actual (visible en UI)
        self.razon           = "Trafico normal"

        # Contadores — empieza posicionado al inicio de la fase ROJA
        self.frames_en_ciclo = (TIEMPO_VERDE_NORMAL + TIEMPO_AMARILLO) * 30
        self.contador_frames = self.frames_en_ciclo

    # ------------------------------------------------------------------
    # Calcula tiempos óptimos según detecciones — NO los aplica aún
    # ------------------------------------------------------------------
    def _calcular_tiempos(self, vehiculos, peatones):

        # PRIORIDAD MÁXIMA: Peatones detectados → rojo largo para autos
        if peatones > 0:
            razon = f"Prioridad peatones ({peatones} detectados)"
            return TIEMPO_VERDE_NORMAL, TIEMPO_ROJO_PEATONES, razon

        # Muchos autos → verde extendido dinámico (2s por auto sobre umbral)
        if vehiculos > UMBRAL_AUTOS_ALTO:
            extras = vehiculos - UMBRAL_AUTOS_ALTO
            verde  = TIEMPO_VERDE_BASE + extras * SEGUNDOS_POR_AUTO
            verde  = min(verde, TIEMPO_VERDE_MAXIMO)
            razon  = f"Trafico alto ({vehiculos} autos) -> {verde}s de verde"
            return verde, TIEMPO_ROJO_NORMAL, razon

        # Tráfico moderado
        if vehiculos >= UMBRAL_AUTOS_BAJO:
            razon = f"Trafico moderado ({vehiculos} autos)"
            return TIEMPO_VERDE_MODERADO, TIEMPO_ROJO_NORMAL, razon

        # Poco tráfico — tiempos normales
        razon = f"Trafico normal ({vehiculos} autos)"
        return TIEMPO_VERDE_NORMAL, TIEMPO_ROJO_NORMAL, razon

    # ------------------------------------------------------------------
    # Llamar cada frame
    # ------------------------------------------------------------------
    def actualizar(self, vehiculos, peatones):
        fps             = self.fps
        frames_verde    = self.tiempo_verde    * fps
        frames_amarillo = self.tiempo_amarillo * fps
        frames_rojo     = self.tiempo_rojo     * fps
        duracion_ciclo  = frames_verde + frames_amarillo + frames_rojo

        pos = self.frames_en_ciclo

        # Estado según posición en el ciclo
        if pos < frames_verde:
            self.estado = VERDE
        elif pos < frames_verde + frames_amarillo:
            self.estado = AMARILLO
        else:
            self.estado = ROJO

        # Avanzar frame
        self.frames_en_ciclo += 1
        self.contador_frames += 1

        # Calcular próximos tiempos (sin aplicar todavía)
        pv, pr, razon     = self._calcular_tiempos(vehiculos, peatones)
        self._prox_verde  = pv
        self._prox_rojo   = pr
        self._prox_razon  = razon

        # Fin de ciclo → aplicar los tiempos calculados para el siguiente
        if self.frames_en_ciclo >= duracion_ciclo:
            self.frames_en_ciclo = 0
            self.tiempo_verde    = self._prox_verde
            self.tiempo_rojo     = self._prox_rojo
            self.razon           = self._prox_razon

        return self.estado

    # ------------------------------------------------------------------
    # Segundos restantes del estado actual
    # ------------------------------------------------------------------
    def segundos_restantes(self):
        fps             = self.fps
        frames_verde    = self.tiempo_verde    * fps
        frames_amarillo = self.tiempo_amarillo * fps
        frames_rojo     = self.tiempo_rojo     * fps
        pos             = self.frames_en_ciclo

        if self.estado == VERDE:
            restante = frames_verde - pos
        elif self.estado == AMARILLO:
            restante = frames_verde + frames_amarillo - pos
        else:
            restante = frames_verde + frames_amarillo + frames_rojo - pos

        return max(0, int(restante / fps))

    # ------------------------------------------------------------------
    # Preview del próximo ciclo (para la UI)
    # ------------------------------------------------------------------
    def preview_tiempos(self):
        return self._prox_verde, self._prox_rojo, self._prox_razon