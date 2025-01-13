from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_seeed_python_dht import DHT
from counterfit_shims_grove.grove_led import GroveLed
import json
import paho.mqtt.client as mqtt

sensor = DHT("11", 2)
led = GroveLed(4)

id = 'idmuitoidentico'
client_telemetry_topic = id + '/telemetria'
server_command_topic = id + '/comandos'
client_name = id + 'coisa'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['estado_led_on']:
        led.on()
    else:
        led.off()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

while True:
    _, valortemperatura = sensor.read()
    print("temp:", valortemperatura)

    mqtt_client.publish(client_telemetry_topic, json.dumps({'temp' : valortemperatura}))

    time.sleep(5)
