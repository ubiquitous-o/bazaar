import random
import argparse
from paho.mqtt import client as mqtt


parser = argparse.ArgumentParser(description='MQTT Subscriber')
parser.add_argument('--host', type=str, default='localhost', help='MQTT Broker host')
parser.add_argument('--port', type=int, default=1883, help='MQTT Broker port')
parser.add_argument('--topic', type=str, default='arm/left', help='MQTT Topic')
args = parser.parse_args()

broker = args.host
port = args.port
topic = args.topic

client_id = 'mqtt-' + str(random.randint(0, 1000))

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
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()