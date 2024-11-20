import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import time
import threading
import colorsys
import seaborn as sns

# Classe Sensor para simular sensores de pressão, fluxo e vazamento
class Sensor:
    def __init__(self, sensor_id, sensor_type):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.value = 0

    def read_data(self):
        if self.sensor_type == 'pressure':
            self.value = random.uniform(400, 800)  # Pressão entre 400 e 800 kPa
        elif self.sensor_type == 'flow':
            self.value = random.uniform(250, 290)  # Fluxo entre 250 e 290 L/min
        elif self.sensor_type == 'leakage':
            self.value = random.choices([200, 150], weights=[0.8, 0.2])[0]  # Vazamento com peso
        return self.value

# Classe para gerenciar o sistema de monitoramento
class WaterManagementSystem:
    def __init__(self, sensors):
        self.sensors = sensors
        self.running = True

    def monitor_sensors(self):
        while self.running:
            for sensor in self.sensors:
                sensor.read_data()
            time.sleep(2)

    def stop_monitoring(self):
        self.running = False

# Função de animação para gráfico de linha
def animate_line(i, sensor, x_data, y_data, start_time, ax):
    value = sensor.read_data()
    y_data.append(value)
    x_data.append(time.time() - start_time)
    ax.clear()

    hue = (i % 100) / 100.0
    rgb_color = colorsys.hsv_to_rgb(hue, 1, 0.8)
    
    ax.plot(x_data, y_data, color=rgb_color, linewidth=2)
    ax.set_title(f"Gráfico de Linha: Sensor {sensor.sensor_id} ({sensor.sensor_type})", fontsize=12)
    ax.set_xlabel("Tempo (s)", fontsize=10)
    ax.set_ylabel("Valor do Sensor", fontsize=10)
    ax.grid(True)

# Função de animação para gráfico de dispersão
def animate_scatter(i, sensor, x_data, y_data, start_time, ax):
    value = sensor.read_data()
    y_data.append(value)
    x_data.append(time.time() - start_time)
    ax.clear()

    hue = (i % 100) / 100.0
    rgb_color = colorsys.hsv_to_rgb(hue, 1, 0.8)
    
    ax.scatter(x_data, y_data, color=rgb_color, s=50)
    
    if len(x_data) > 1:
        coefficients = np.polyfit(x_data, y_data, 1)
        polynomial = np.poly1d(coefficients)
        regression_line = polynomial(x_data)
        ax.plot(x_data, regression_line, color='red', linestyle='--', label='Regressão Linear')

    ax.set_title(f"Gráfico de Dispersão: Sensor {sensor.sensor_id} ({sensor.sensor_type})", fontsize=12)
    ax.set_xlabel("Tempo (s)", fontsize=10)
    ax.set_ylabel("Valor do Sensor", fontsize=10)
    ax.legend()
    ax.grid(True)

# Função de animação para gráfico de pizza
def animate_pie(i, sensors, ax):
    ax.clear()
    values = [sensor.read_data() for sensor in sensors]

    colors = [colorsys.hsv_to_rgb((i + j) / len(sensors), 1, 0.8) for j in range(len(sensors))]
    ax.pie(values, labels=[f'Sensor {sensor.sensor_id} ({sensor.sensor_type})' for sensor in sensors], 
           colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title("Gráfico de Pizza: Leituras dos Sensores", fontsize=12)
    ax.axis('equal')

# Função de animação para gráfico de densidade
def animate_density(i, sensors, ax):
    ax.clear()
    values = [sensor.read_data() for sensor in sensors]
    sns.kdeplot(values, ax=ax, fill=True, color='skyblue')
    ax.set_title("Gráfico de Densidade", fontsize=12)
    ax.set_xlabel("Valor do Sensor", fontsize=10)
    ax.set_ylabel("Densidade", fontsize=10)
    ax.grid(True)

# Função de animação para gráfico de barras (Qualidade da Água)
def animate_bar(i, sensors, ax):
    ax.clear()
    values = [sensor.read_data() for sensor in sensors]
    labels = [f'Sensor {sensor.sensor_id} ({sensor.sensor_type})' for sensor in sensors]
    colors = ['skyblue', 'green', 'orange']
    
    ax.bar(labels, values, color=colors)
    ax.set_title("Gráfico de Barras: Qualidade da Água", fontsize=12)
    ax.set_xlabel("Tipo de Sensor", fontsize=10)
    ax.set_ylabel("Valor", fontsize=10)
    ax.grid(True)

# Inicializando os sensores
sensors = [Sensor(sensor_id=1, sensor_type='pressure'),
           Sensor(sensor_id=2, sensor_type='flow'),
           Sensor(sensor_id=3, sensor_type='leakage')]

# Dados para gráficos
x_data, y_data = [], []
start_time = time.time()

# Configuração das figuras e subplots para gráficos
fig1, ax1 = plt.subplots()  # Gráfico de Linha
fig2, ax2 = plt.subplots()  # Gráfico de Dispersão
fig3, ax3 = plt.subplots()  # Gráfico de Pizza
fig4, ax4 = plt.subplots()  # Gráfico de Densidade
fig5, ax5 = plt.subplots()  # Gráfico de Barras

# Configurando as animações
ani_line = animation.FuncAnimation(fig1, animate_line, fargs=(sensors[0], x_data, y_data, start_time, ax1), interval=1000)
ani_scatter = animation.FuncAnimation(fig2, animate_scatter, fargs=(sensors[0], x_data, y_data, start_time, ax2), interval=1000)
ani_pie = animation.FuncAnimation(fig3, animate_pie, fargs=(sensors, ax3), interval=1000)
ani_density = animation.FuncAnimation(fig4, animate_density, fargs=(sensors, ax4), interval=1000)
ani_bar = animation.FuncAnimation(fig5, animate_bar, fargs=(sensors, ax5), interval=1000)

# Exibe todos os gráficos
plt.show()
