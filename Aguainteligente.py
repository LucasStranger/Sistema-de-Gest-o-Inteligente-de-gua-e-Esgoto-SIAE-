import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
        self.running = True  # Variável para controlar o monitoramento

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

# Função de animação
def animate(i, sensor, x_data, y_data, start_time):
    value = sensor.read_data()
    y_data.append(value)
    x_data.append(time.time() - start_time)

    ax.clear()
    
    # Definindo a cor com base em HSV
    hue = (i % 100) / 100.0
    rgb_color = colorsys.hsv_to_rgb(hue, 1, 1)
    
    ax.plot(x_data, y_data, color=rgb_color)
    ax.set_title(f"Monitoramento do sensor {sensor.sensor_id} ({sensor.sensor_type})")
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Valor do Sensor")

# Configuração para plotar o gráfico com animação
fig, ax = plt.subplots()
x_data, y_data = [], []
start_time = time.time()

# Exemplo de sensor de fluxo
sensor_example = Sensor(sensor_id=4, sensor_type='flow')

# Configura a animação
ani = animation.FuncAnimation(
    fig, 
    animate, 
    fargs=(sensor_example, x_data, y_data, start_time), 
    interval=1000
)

# Criando sensores adicionais
sensor1 = Sensor(sensor_id=1, sensor_type='pressure')
sensor2 = Sensor(sensor_id=2, sensor_type='flow')
sensor3 = Sensor(sensor_id=3, sensor_type='leakage')

# Lista de sensores
sensors = [sensor1, sensor2, sensor3]
water_management_system = WaterManagementSystem(sensors)

# Iniciando o monitoramento dos sensores
start_monitoring(water_management_system)

# Definindo um tempo limite para o monitoramento
def stop_system_after_delay(delay):
    time.sleep(delay)
    water_management_system.stop_monitoring()
    print("Monitoramento encerrado.")

# Iniciar o timer para encerrar o monitoramento após 20 segundos
threading.Thread(target=stop_system_after_delay, args=(20,)).start()

# Exibe o gráfico
plt.show()
