import paho.mqtt.client as mqtt
import argparse
import random
import time
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


def publish(client, msg):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client, args.msg)


if __name__ == '__main__':
    run()