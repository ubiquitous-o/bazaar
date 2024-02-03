import paho.mqtt.client as mqtt
import argparse
 
# ブローカーに接続できたときの処理
def on_connect(client,userdata, flag, rc, topic):
    print("Connected with result code " + str(rc))  # 接続できた旨表示
    client.subscribe(topic)  # subするトピックを設定 

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, rc):
    if  rc != 0:
        print("Unexpected disconnection.")

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
    # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
    print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MQTT Subscriber')
    parser.add_argument('--host', type=str, default='localhost', help='MQTT Broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT Broker port')
    parser.add_argument('--topic', type=str, default='arm/left', help='MQTT Topic')
    args = parser.parse_args()

    # MQTTの接続設定
    client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
    client.on_connect = on_connect(topic=args.topic)         # 接続時のコールバック関数を登録
    client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
    client.on_message = on_message         # メッセージ到着時のコールバック

    client.connect(args.host, args.port, 60)  

    client.loop_forever()