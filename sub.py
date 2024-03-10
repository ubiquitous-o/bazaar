import random
import argparse
from paho.mqtt import client as mqtt
import subprocess
import servo
import sys
import pigpio


parser = argparse.ArgumentParser(description='MQTT Subscriber')
parser.add_argument('--host', type=str, default='localhost', help='MQTT Broker host')
parser.add_argument('--port', type=int, default=1883, help='MQTT Broker port')
# parser.add_argument('--topic', type=str, default='arm/left', help='MQTT Topic')
args = parser.parse_args()

broker = args.host
port = args.port
# topic = args.topic

client_id = 'mqtt-' + str(random.randint(0, 1000))

global serv_head
global serv_arml
global serv_armr
global light

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        global serv_head
        global serv_arml
        global serv_armr
        global light

        print("Received `{}` from `{}` topic".format(msg.payload.decode(), msg.topic))
        
        if msg.topic == 'head':
            data = int(msg.payload.decode())
            if data > 0:
                serv_head.set_angle(int(msg.payload.decode()))
            else:
                serv_head.stop()

        elif msg.topic == 'arm/left':
            data = int(msg.payload.decode())
            if data > 0:
                serv_arml.set_angle(int(msg.payload.decode()))
            else:
                serv_arml.stop()


        elif msg.topic == 'arm/right':
            data = int(msg.payload.decode())
            if data > 0:
                serv_armr.set_angle(int(msg.payload.decode()))
            else:
                serv_armr.stop()
                sys.exit("bye")
        elif msg.topic == 'eye':
            data = int(msg.payload.decode())
            if data > 0:
                light.write(2, 1)
                print("light on")
            else:
                light.write(2, 0)
                print("light off")
        else:
            pass
        
        
    client.subscribe("head")
    client.subscribe("arm/left")
    client.subscribe("arm/right")
    client.on_message = on_message


def run():
    client = connect_mqtt()
    global serv_head
    global serv_arml
    global serv_armr
    global light

    serv_head = servo.ServoMotor(pin=18)
    serv_head.init()
    serv_arml = servo.ServoMotor(pin=23)
    serv_arml.init()
    serv_armr = servo.ServoMotor(pin=24)
    serv_armr.init()

    light = pigpio.pi()
    light.set_mode(2,pigpio.OUTPUT)

    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
