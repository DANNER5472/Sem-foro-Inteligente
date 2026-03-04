import numpy as np

VERDE    = "VERDE"
AMARILLO = "AMARILLO"
ROJO     = "ROJO"

class ControladorSemaforo:
    def __init__(self):
     
        self.Kp = 0.8
        self.Ki = 0.15
        self.Kd = 0.05

    
        self.t_min_verde = 8
        self.t_max_verde = 30
        self.t_min_rojo  = 8
        self.t_max_rojo  = 25
        self.tiempo_amarillo = 3

        
        self.tiempo_verde    = 10
        self.tiempo_rojo     = 10
        self.estado          = VERDE
        self.contador_frames = 0
        self.fps             = 30

       
        self.integral_v       = 0.0
        self.error_anterior_v = 0.0
        self.integral_r       = 0.0
        self.error_anterior_r = 0.0

        
        self.MAX_VEHICULOS = 15
        self.MAX_PEATONES  = 8
        self.setpoint_v    = 0.3
        self.setpoint_p    = 0.2

    def _pid(self, error, integral, error_anterior, dt=1.0):
        P        = self.Kp * error
        integral = float(np.clip(integral + error * dt, -10, 10))
        I        = self.Ki * integral
        D        = self.Kd * (error - error_anterior) / dt
        return P + I + D, integral, error

    def ajustar_tiempos(self, vehiculos, peatones):

        densidad_v = min(vehiculos / self.MAX_VEHICULOS, 1.0)
        densidad_p = min(peatones  / self.MAX_PEATONES,  1.0)


        error_v = densidad_v - self.setpoint_v
        salida_v, self.integral_v, self.error_anterior_v = self._pid(
            error_v, self.integral_v, self.error_anterior_v)
        self.tiempo_verde = int(np.clip(
            self.t_min_verde + salida_v * self.t_max_verde,
            self.t_min_verde, self.t_max_verde))

        error_p = densidad_p - self.setpoint_p
        salida_p, self.integral_r, self.error_anterior_r = self._pid(
            error_p, self.integral_r, self.error_anterior_r)
        self.tiempo_rojo = int(np.clip(
            self.t_min_rojo + salida_p * self.t_max_rojo,
            self.t_min_rojo, self.t_max_rojo))

        if densidad_p > 0.6:
            self.tiempo_rojo  = max(self.tiempo_rojo, 18)
            self.tiempo_verde = min(self.tiempo_verde, 10)

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