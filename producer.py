import logging
from queue import Queue
from json import dumps
import paho.mqtt.client as mqtt
from serial import Serial
from protocol.package.package import Package

message_received = ''

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    logging.info(f"mensaje recibido {message_received}")


client = mqtt.Client(client_id="py-producer")
client.on_message=on_message
client.connect(host="broker.hivemq.com", port=1883)

def worker(input_queue: Queue,uart):
    while True:
        payload = input_queue.get()
        client.publish(
            topic="sda/esp32",
            payload=dumps(payload),
        )
        logging.info(f"sending payload over mqttt {dumps(payload)}")        
        client.subscribe(topic="sda/led")
       # uart.write(b"logg")
        enc = bytearray()
        enc.extend(bytearray.fromhex(b"7E037E010080"))
        apa = bytearray()
        apa.extend(bytearray.fromhex(b"7E037E000081"))
        if message_received == enc:
            uart.write(b"7E037E000081")
        elif message_received == apa:
            uart.write(b"7E037E010080")
        logging.info("data send")   
        

        





