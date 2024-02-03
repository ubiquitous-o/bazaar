import paho.mqtt.client as mqtt
import argparse

def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MQTT Publisher')
    parser.add_argument('--host', type=str, default='localhost', help='MQTT Broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT Broker port')
    parser.add_argument('--topic', type=str, default='arm/left', help='MQTT Topic')
    parser.add_argument('--msg', type=str, default='Hello, World!', help='MQTT Message')
    args = parser.parse_args()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    client.connect(args.host, args.port, 60)

    client.loop_start()

    client.publish(args.topic, args.msg)