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
            self.value = random.uniform(400, 800)  # Aumentando a pressão para entre 1.0 e 3.0 bar
        elif self.sensor_type == 'flow':
            self.value = random.uniform(250, 290)  # Fluxo de água em litros/minuto
        elif self.sensor_type == 'leakage':
            self.value = random.choices([200, 150], weights=[0.8, 0.2])[0]  # Aumentando a chance de vazamento
        return self.value

# Classe para gerenciar o sistema de monitoramento de água
class WaterManagementSystem:
    def __init__(self, sensors):
        self.sensors = sensors
        self.running = True

    def monitor_sensors(self):
        while self.running:
            for sensor in self.sensors:
                sensor_value = sensor.read_data()
                if sensor.sensor_type == 'leakage' and sensor_value == 1:
                    print(f"ALERTA: Vazamento detectado pelo sensor {sensor.sensor_id}!")
                    self.handle_leakage(sensor.sensor_id)
                elif sensor.sensor_type == 'pressure' and (sensor_value < 0.7 or sensor_value > 1.3):
                    print(f"ALERTA: Pressão fora do normal no sensor {sensor.sensor_id} - valor: {sensor_value:.2f} bar")
                elif sensor.sensor_type == 'flow' and sensor_value < 80:
                    print(f"ALERTA: Fluxo de água baixo detectado no sensor {sensor.sensor_id} - valor: {sensor_value:.2f} L/min")
            time.sleep(2)

    def handle_leakage(self, sensor_id):
        print(f"Executando ação: Fechando válvula do sensor {sensor_id} para evitar desperdício de água.")

    def stop_monitoring(self):
        self.running = False

# Função para iniciar o monitoramento em uma nova thread
def start_monitoring(system):
    monitoring_thread = threading.Thread(target=system.monitor_sensors)
    monitoring_thread.start()

# Função de animação para o gráfico de Linha
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

# Função de animação para o gráfico de Dispersão
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

# Função de animação para o gráfico de Pizza RGB
def animate_pie(i, sensors, ax):
    ax.clear()
    values = [sensor.read_data() for sensor in sensors]

    # Cores RGB para o gráfico de pizza, mudando com o tempo
    colors = [colorsys.hsv_to_rgb((i + j) / len(sensors), 1, 0.8) for j in range(len(sensors))]
    
    ax.pie(values, labels=[f'Sensor {sensor.sensor_id} ({sensor.sensor_type})' for sensor in sensors], 
           colors=colors, autopct='%1.1f%%', startangle=90)
    
    ax.set_title("Gráfico de Pizza: Leituras dos Sensores", fontsize=12)
    ax.axis('equal')

# Função de animação para o gráfico de Densidade
def animate_density(i, sensors, ax):
    ax.clear()
    values = [sensor.read_data() for sensor in sensors]
    
    # Plotando gráfico de densidade
    sns.kdeplot(values, ax=ax, fill=True, color='skyblue')
    ax.set_title("Gráfico de Densidade", fontsize=12)
    ax.set_xlabel("Valor do Sensor", fontsize=10)
    ax.set_ylabel("Densidade", fontsize=10)
    ax.grid(True)

# Inicializando os sensores
sensors = [Sensor(sensor_id=1, sensor_type='pressure'),
           Sensor(sensor_id=2, sensor_type='flow'),
           Sensor(sensor_id=3, sensor_type='leakage')]

# Dados para gráficos
x_data, y_data = [], []
start_time = time.time()

# Configuração das figuras e subplots para os gráficos de Linha, Dispersão, Pizza e Densidade
fig1, ax1 = plt.subplots()  # Gráfico de Linha
fig2, ax2 = plt.subplots()  # Gráfico de Dispersão
fig3, ax3 = plt.subplots()  # Gráfico de Pizza
fig4, ax4 = plt.subplots()  # Gráfico de Densidade

# Configurando as animações
ani_line = animation.FuncAnimation(fig1, animate_line, fargs=(sensors[0], x_data, y_data, start_time, ax1), interval=1000)
ani_scatter = animation.FuncAnimation(fig2, animate_scatter, fargs=(sensors[0], x_data, y_data, start_time, ax2), interval=1000)
ani_pie = animation.FuncAnimation(fig3, animate_pie, fargs=(sensors, ax3), interval=1000)
ani_density = animation.FuncAnimation(fig4, animate_density, fargs=(sensors, ax4), interval=1000)

# Criando sistema de monitoramento com sensores
water_management_system = WaterManagementSystem(sensors)

# Iniciar o monitoramento em paralelo
start_monitoring(water_management_system)

# Exibe todos os gráficos
plt.show()
