from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

connection_string = "HostName=hubFranc.azure-devices.net;DeviceId=soil-moisture-sensor-franc;SharedAccessKey=b26mHBZn7N3woqlU3EK24Oh83IKIHQYKaHq2jO6Ou1o="
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
print('Connecting')
device_client.connect()
print('Connected')

adc = ADC()
relay = GroveRelay(5)

id = '202218491'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'soilmoisturesensor_client'

def handle_method_request(request):
	print("Direct method received - ", request.name)

	if request.name == "relay_on":
		relay.on()
	elif request.name == "relay_off":
		relay.off()    
		method_response = MethodResponse.create_from_method_request(request, 200)
		device_client.send_method_response(method_response)

device_client.on_method_request_received = handle_method_request

while True:
	soil_moisture = adc.read(0)
	print("Soil moisture:", soil_moisture)


	message = Message(json.dumps({ 'soil_moisture': soil_moisture }))
	device_client.send_message(message)
	time.sleep(10)
