import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
import argparse

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

# publishが完了したときの処理
def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MQTT Publisher')
    parser.add_argument('--host', type=str, default='localhost', help='MQTT Broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT Broker port')
    parser.add_argument('--topic', type=str, default='arm/left', help='MQTT Topic')
    parser.add_argument('--msg', type=str, default='Hello, World!', help='MQTT Message')
    args = parser.parse_args()

    client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
    client.on_connect = on_connect         # 接続時のコールバック関数を登録
    client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
    client.on_publish = on_publish         # メッセージ送信時のコールバック

    client.connect(args.host, args.port, 60)  # 接続先は自分自身

    # 通信処理スタート
    client.loop_start()    # subはloop_forever()だが，pubはloop_start()で起動だけさせる

    client.publish(args.topic, args.msg)    # トピック名とメッセージを決めて送信
