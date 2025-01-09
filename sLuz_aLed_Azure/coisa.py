import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
import json

CounterFitConnection.init('127.0.0.1', 5000)
connection_string = "<HostName-conKey>"
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
light_sensor = GroveLightSensor(0)
led = GroveLed(5)

print('Connecting')
device_client.connect()
print('Connected')

id = 'testepratico-sensor'

client_telemetry_topic = id + '/telemetry'
client_name = id + 'nightlight_client'


def handle_method_request(request):
	print("Direct method received - ", request.name)

	if request.name == "led_on":
		led.on()
	elif request.name == "led_off":
		led.off()    
	method_response = MethodResponse.create_from_method_request(request, 200)
	device_client.send_method_response(method_response)

device_client.on_method_request_received = handle_method_request    
    
while True:
	light = light_sensor.light
	telemetry = json.dumps({'light' : light})
	print(telemetry)
    
	message = Message(json.dumps({ 'light': light }))
	device_client.send_message(message)
	time.sleep(10)
	
