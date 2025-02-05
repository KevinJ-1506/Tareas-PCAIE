import numpy as np
import matplotlib.pyplot as plt

# Generar valores para x
x = np.linspace(0, 2 * np.pi, 1000)  # De 0 a 2pi con 1000 puntos

# Calcular la función seno de x
y = np.sin(x)

# Crear la gráfica
plt.figure(figsize=(8, 6))  # Tamaño de la figura
plt.plot(x, y, label="y = sin(x)", color="blue")

# Agregar título y etiquetas
plt.title("Gráfica de la función seno", fontsize=16)
plt.xlabel("Eje X", fontsize=12)
plt.ylabel("Eje Y", fontsize=12)

# Agregar una cuadrícula y leyenda
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(fontsize=12)

# Mostrar la gráfica
plt.show()
