import paho.mqtt.client as mqtt
import argparse
 

def on_connect(client,userdata, flag, rc, topic):
    print("Connected with result code " + str(rc))
    client.subscribe(topic) 

def on_disconnect(client, userdata, rc):
    if  rc != 0:
        print("Unexpected disconnection.")

def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MQTT Subscriber')
    parser.add_argument('--host', type=str, default='localhost', help='MQTT Broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT Broker port')
    parser.add_argument('--topic', type=str, default='arm/left', help='MQTT Topic')
    args = parser.parse_args()

    client = mqtt.Client()
    client.on_connect = on_connect(topic=args.topic)
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(args.host, args.port, 60)  

    client.loop_forever()