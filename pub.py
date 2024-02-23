import paho.mqtt.client as mqtt
import argparse
import random
import time
import keyboard

parser = argparse.ArgumentParser(description='MQTT Pubrisher')
parser.add_argument('--host', type=str, default='localhost', help='MQTT Broker host')
parser.add_argument('--port', type=int, default=1883, help='MQTT Broker port')
parser.add_argument('--topic', type=str, default='arm/left', help='MQTT Topic')
parser.add_argument('--msg', type=str, default='Helloooooooooo', help='MQTT Msg')

args = parser.parse_args()

broker = args.host
port = args.port
topic = args.topic

client_id = 'mqtt-' + str(random.randint(0, 1000))

def connect_mqtt():
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


def publish(client, msg, topic):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    while True:
        if keyboard.is_pressed('q'):
            break
        elif keyboard.is_pressed('w'):
            args.msg = 'w'
            args.topic = 'arm/forward'
            publish(client, args.msg, args.topic)

        elif keyboard.is_pressed('s'):
            args.msg = 's'
            args.topic = 'arm/backward'
            publish(client, args.msg, args.topic)

        elif keyboard.is_pressed('a'):
            args.msg = 'a'
            args.topic = 'arm/left'
            publish(client, args.msg, args.topic)
        elif keyboard.is_pressed('d'):
            args.msg = 'd'
            args.topic = 'arm/right'
            publish(client, args.msg, args.topic)
        else:
            print("no key pressed")
            pass

if __name__ == '__main__':
    run()