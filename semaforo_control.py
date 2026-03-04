"""
Análisis Matemático - Control Inteligente de Semáforos
Usando python-control
Proyecto: Control de Tráfico con IA - Bolivia
"""

import numpy as np
import matplotlib.pyplot as plt
import control


K   = 60   
tau = 5    

G = control.tf([K], [tau, 1])
print("=" * 50)
print("  ANÁLISIS MATEMÁTICO - SEMÁFORO INTELIGENTE")
print("=" * 50)
print(f"\n📌 Planta G(s):\n{G}")

Kp, Ki, Kd = 0.8, 0.15, 0.05
C = control.tf([Kd, Kp, Ki], [1, 0])
print(f"\n📌 Controlador PID C(s):\n{C}")

lazo_abierto = control.series(C, G)
lazo_cerrado = control.feedback(lazo_abierto, 1)

polos   = control.poles(lazo_cerrado)
estable = all(p.real < 0 for p in polos)
print(f"\n✅ Polos: {polos}")
print(f"✅ Sistema: {'ESTABLE' if estable else 'INESTABLE'}")

info = control.step_info(lazo_cerrado)
print(f"✅ Tiempo de establecimiento: {info['SettlingTime']:.2f}s")
print(f"✅ Sobreimpulso: {info['Overshoot']:.2f}%")





t_step, y_step = control.step_response(lazo_cerrado, T=t)
ax1 = axes[0, 0]
ax1.plot(t_step, y_step * K, 'b-', linewidth=2, label='Tiempo de verde')
ax1.axhline(y=K, color='r', linestyle='--', label=f'Referencia ({K}s)')
ax1.fill_between(t_step, y_step * K, alpha=0.1, color='blue')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Tiempo de verde (s)')
ax1.set_title('Respuesta al Escalón')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.annotate(f"Ts={info['SettlingTime']:.1f}s\nMp={info['Overshoot']:.1f}%",
             xy=(0.65, 0.15), xycoords='axes fraction',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)

# --- Tráfico Variable (escenario real) ---
densidad = np.zeros_like(t)
densidad[t < 10]                        = 0.1  # madrugada
densidad[(t >= 10) & (t < 25)]          = 0.9  # hora pico
densidad[(t >= 25) & (t < 40)]          = 0.6  # moderado
densidad[(t >= 40) & (t < 50)]          = 0.3  # tarde
densidad[t >= 50]                       = 0.1  # noche

t_resp, y_resp = control.forced_response(lazo_cerrado, T=t, U=densidad)
tiempo_verde = np.clip(y_resp * K, 8, K)

ax2 = axes[0, 1]
ax2.plot(t, densidad * K, 'r--', linewidth=1.5, label='Densidad detectada ×60', alpha=0.7)
ax2.plot(t, tiempo_verde, 'b-', linewidth=2, label='Tiempo de verde (PID)')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Segundos')
ax2.set_title('Respuesta a Tráfico Variable\n(Escenario Real)')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# --- Diagrama de Bode ---
omega = np.logspace(-2, 2, 500)
mag, phase, omega_out = control.bode(lazo_abierto, omega, plot=False)
ax3 = axes[1, 0]
ax3.semilogx(omega_out, 20 * np.log10(mag), 'b-', linewidth=2)
ax3.axhline(y=0, color='r', linestyle='--', label='0 dB')
ax3.set_xlabel('Frecuencia (rad/s)')
ax3.set_ylabel('Magnitud (dB)')
ax3.set_title('Diagrama de Bode\n(Lazo Abierto)')
ax3.legend()
ax3.grid(True, which='both', alpha=0.3)

# --- Con vs Sin PID ---
_, y_sin = control.step_response(control.feedback(G, 1), T=t)
_, y_con = control.step_response(lazo_cerrado, T=t)
ax4 = axes[1, 1]
ax4.plot(t, y_sin * K, 'r-', linewidth=2, label='Sin PID', alpha=0.8)
ax4.plot(t, y_con * K, 'b-', linewidth=2, label='Con PID')
ax4.axhline(y=K, color='gray', linestyle='--', label='Referencia')
ax4.set_xlabel('Tiempo (s)')
ax4.set_ylabel('Tiempo de verde (s)')
ax4.set_title('Comparación: Con vs Sin PID')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('semaforo_control_analisis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n📊 Gráfica guardada: semaforo_control_analisis.png")