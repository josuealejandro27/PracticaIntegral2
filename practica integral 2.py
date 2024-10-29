from machine import Pin, I2C, PWM
import dht
import ssd1306
import time

# Definir pines
DHT_PIN = Pin(14)              
buzzer = PWM(Pin(23))         
red_pin = PWM(Pin(18))         
green_pin = PWM(Pin(19))      
blue_pin = PWM(Pin(17))        

# Configurar la pantalla OLED
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Crear objeto DHT11
sensor = dht.DHT11(DHT_PIN)

# Definir el rango de temperatura y humedad para activar la alarma
TEMP_MAX = 30.0
HUM_MAX = 70.0

# Definición de notas (frecuencias)
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392

# Melodía simple de 5 notas
simple_melody = [
    (C4, 400),  
    (D4, 400),  
    (E4, 400),  
    (F4, 400),  
    (G4, 400)   
]

# Función para reproducir la melodía
def play_melody(melody):
    for note, duration in melody:
        if note == 0:
            buzzer.duty(0)  # Silencio para pausas
        else:
            buzzer.freq(note)  # Frecuencia de la nota
            buzzer.duty(512)    # Volumen del sonido (ajusta si es necesario)
        time.sleep_ms(duration)  # Duración específica de cada nota
    buzzer.duty(0)  # Apagar el buzzer al finalizar

# Función para actualizar la pantalla OLED
def actualizar_oled(temp, hum):
    oled.fill(0)  
    oled.text("Temperatura:", 0, 0)
    oled.text("{:.1f} C".format(temp), 0, 10)
    oled.text("Humedad:", 0, 30)
    oled.text("{:.1f} %".format(hum), 0, 40)
    oled.show()

# Función para controlar el LED RGB
def cambiar_color_led(rojo, verde, azul):
    red_pin.duty(rojo)
    green_pin.duty(verde)
    blue_pin.duty(azul)

# Función principal
while True:
    try:
        # Leer temperatura y humedad del DHT11
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        # Mostrar valores en la OLED siempre
        actualizar_oled(temp, hum)

        # Condiciones de alarma
        if temp > TEMP_MAX or hum > HUM_MAX:
            # Temperatura o humedad demasiado altas, encender alerta
            cambiar_color_led(1023, 0, 0)  # LED rojo
            play_melody(simple_melody)      # Reproducir melodía
        elif temp <= 28:  
            cambiar_color_led(0, 1023, 1023)  # LED azul claro
        else:
            # Todo dentro del rango, mostrar LED verde
            cambiar_color_led(0, 1023, 0)  
            buzzer.duty(0)                  # Apagar buzzer

        time.sleep(1) 
    except OSError as e:
        print("Error al leer del DHT11")
