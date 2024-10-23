import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import time
import threading
import colorsys

# Classe Sensor para simular sensores de pressão, fluxo e vazamento
class Sensor:
    def __init__(self, sensor_id, sensor_type):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.value = 0

    def read_data(self):
        if self.sensor_type == 'pressure':
            self.value = random.uniform(0.5, 2.0)  # Pressão da água em bar
        elif self.sensor_type == 'flow':
            self.value = random.uniform(100, 500)  # Fluxo de água em litros/minuto
        elif self.sensor_type == 'leakage':
            self.value = random.choice([0, 1])  # 0: Sem vazamento, 1: Vazamento detectado
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
                elif sensor.sensor_type == 'pressure' and (sensor_value < 0.8 or sensor_value > 1.5):
                    print(f"ALERTA: Pressão fora do normal no sensor {sensor.sensor_id} - valor: {sensor_value:.2f} bar")
                elif sensor.sensor_type == 'flow' and sensor_value < 150:
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
    rgb_color = colorsys.hsv_to_rgb(hue, 1, 1)
    
    ax.plot(x_data, y_data, color=rgb_color)
    ax.set_title(f"Gráfico de Linha: Sensor {sensor.sensor_id} ({sensor.sensor_type})")
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Valor do Sensor")

# Função de animação para o gráfico de Dispersão
def animate_scatter(i, sensor, x_data, y_data, start_time, ax):
    value = sensor.read_data()
    y_data.append(value)
    x_data.append(time.time() - start_time)

    ax.clear()

    hue = (i % 100) / 100.0
    rgb_color = colorsys.hsv_to_rgb(hue, 1, 1)
    
    ax.scatter(x_data, y_data, color=rgb_color)
    
    # Adicionando regressão linear
    if len(x_data) > 1:  # Verifica se há dados suficientes para regressão
        # Calcular os coeficientes da regressão linear
        coefficients = np.polyfit(x_data, y_data, 1)
        polynomial = np.poly1d(coefficients)
        regression_line = polynomial(x_data)

        ax.plot(x_data, regression_line, color='red', linestyle='--', label='Regressão Linear')

    ax.set_title(f"Gráfico de Dispersão: Sensor {sensor.sensor_id} ({sensor.sensor_type})")
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Valor do Sensor")
    ax.legend()

# Inicializando o sensor 4
sensor_example = Sensor(sensor_id=4, sensor_type='flow')

# Dados para gráficos
x_data, y_data = [], []
start_time = time.time()

# Configuração das figuras e subplots para os gráficos de Linha e Dispersão
fig1, ax1 = plt.subplots()  # Gráfico de Linha
fig2, ax2 = plt.subplots()  # Gráfico de Dispersão

# Configurando as animações
ani_line = animation.FuncAnimation(fig1, animate_line, fargs=(sensor_example, x_data, y_data, start_time, ax1), interval=1000)
ani_scatter = animation.FuncAnimation(fig2, animate_scatter, fargs=(sensor_example, x_data, y_data, start_time, ax2), interval=1000)

# Criando sistema de monitoramento com sensor 4
sensors = [sensor_example]
water_management_system = WaterManagementSystem(sensors)

# Iniciar o monitoramento em paralelo
start_monitoring(water_management_system)

# Exibe todos os gráficos
plt.show()
