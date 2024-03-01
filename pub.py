import paho.mqtt.client as mqtt
import argparse
import random
import time
from pynput.keyboard import Listener


parser = argparse.ArgumentParser(description='MQTT Pubrisher')
parser.add_argument('--host', type=str, default='localhost', help='MQTT Broker host')
parser.add_argument('--port', type=int, default=1883, help='MQTT Broker port')

args = parser.parse_args()

broker = args.host
port = args.port

client_id = 'mqtt-' + str(random.randint(0, 1000))
global client

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    global client
    client = mqtt.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(msg, topic):
    global client
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def run():
    print("please wait for the connection to be established...")
    global client
    client = connect_mqtt()
    client.loop_start()

def on_press(key):
    print(key)
    if key.char == 'w':
        msg = 'w'
        topic = 'arm/forward'
        publish(msg, topic)
    elif key.char == 's':
        msg = 's'
        topic = 'arm/backward'
        publish(msg, topic)
    elif key.char == 'a':
        msg = '100'
        topic = 'arm/left'
        publish(msg, topic)
    elif key.char == 'd':
        msg = 'd'
        topic = 'arm/right'
        publish(msg, topic)

    else:
        print("no key pressed")
        pass



if __name__ == '__main__':
    run()
    with Listener(on_press=on_press) as listener:
        listener.join()