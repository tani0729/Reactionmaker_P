import cv2
import os
import datetime
import time
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import numpy as np
import json
import socket
import pickle
from statistics import stdev, variance, median

HOST='***.***.*.***'
#接続先ホストのポート番号
PORT = 2434
#ソケットから受信するデータのバッファサイズ
BUFSIZE = 4096

#ソケットの作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    #サーバへの接続
    sock.connect((HOST,PORT))
finally:
    pass

headers = {
#FaceAPIに接続,
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '**************************',
}
#返すデータの設定（この場合顔のIDは無し、感情の数値のみ返す）
params = urllib.parse.urlencode({
    'returnFaceId': 'False',
    'returnFaceAttributes': 'emotion'
})
#パソコン内のカメラから動画を取得
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#動画から切り出した画像を一時的に保存するためのフォルダを作成
os.makedirs("Desktop/data/temp", exist_ok=True)

 #取得した動画の表示
n = 0
i = 0
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, dsize=(960, 540))
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#0.1秒ごとに動画から画像を切り出して保存する
    time.sleep(0.1)
    i = i + 1
    write_file_name = "Desktop/data/temp/"+str(i) + ".jpg"
    cv2.imwrite(write_file_name, frame)

    image_file = open(write_file_name,'rb')
    body = image_file.read()
    image_file.close()

#FaceAPIを使って感情を解析する
    try:
        conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        jdata =json.dumps(data, indent=4)
        dec = json.loads(jdata)
        #感情の値が帰ってきた場合、Happinessの平均値を送信する
        if len(dec)>0:
            happy = []
            for emotion in dec:
                faceAttributes =emotion['faceAttributes']
                emotion = faceAttributes['emotion']
                happiness = emotion['happiness']
                happy.append(happiness)
                laugh = median(happy)
                print(dec)
                print(laugh)
            try:
                #サーバへの接続
                mesg = str(laugh)
                #バイトコード化してデータ送信
                sock.send(mesg.encode('utf-8'))
                #データを受信
                receive_msg = sock.recv(BUFSIZE)
            finally:
                pass
        #感情の値が無かった場合、0.0を送信する
        else:
            print(dec)
            try:
                #サーバへの接続
                mesg = "0.0"
                #この行を加えた
                #バイトコード化してデータ送信
                sock.send(mesg.encode('utf-8'))
                #データを受信
                receive_msg = sock.recv(BUFSIZE)
            finally:
                pass

        conn.close()

#FaceAPI接続の際の例外処理
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

# 解析した画像を削除する
    os.remove(write_file_name)

#表示してたウィンドウを閉じる
cv2.destroyWindow('frame')
