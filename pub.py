import paho.mqtt.client as mqtt
import argparse
import random
import time
from pynput.keyboard import Listener, Key


parser = argparse.ArgumentParser(description='MQTT Pubrisher')
parser.add_argument('--host', type=str, default='172.22.22.49', help='MQTT Broker host')
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
    
    try:
        if key == Key.esc:
            print("Exiting...")
            msg = '-100'
            topic = "head"
            publish(msg, topic)
            topic = "arm/left"
            publish(msg, topic)
            topic = "arm/right"
            publish(msg, topic)
            topic = "eye"
            publish(msg,topic)
            
            return False

        # topic1
        elif key.char == 'q':
            msg = '10'
            topic = 'head'
            publish(msg, topic)
        elif key.char == 'e':
            msg = '120'
            topic = 'head'
            publish(msg, topic)
        
        #topic2
        elif key.char == 'a':
            msg = '10'
            topic = 'arm/left'
            publish(msg, topic)
        elif key.char == 'd':
            msg = '120'
            topic = 'arm/left'
            publish(msg, topic)
        
        #topic3
        elif key.char == 'z':
            msg = '10'
            topic = 'arm/right'
            publish(msg, topic)
        elif key.char == 'c':
            msg = '120'
            topic = 'arm/right'
            publish(msg, topic)

        #topic4
        elif key.char == 'o':
            msg = '10'
            topic = 'eye'
            publish(msg, topic)
        elif key.char == 'i':
            msg = '-10'
            topic = 'eye'
            publish(msg, topic)        


        else:
            print("no key pressed")
            pass

    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':
    run()
    with Listener(on_press=on_press) as listener:
        listener.join()
