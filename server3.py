import socket
import pygame.mixer

pygame.mixer.init() #ミキサーの初期化
pygame.mixer.music.load("C:**************laugh.mp3")
#サーバのホスト名(あるいはIPアドレス)
HOST='***.***.*.***'
#ポート番号
PORT = 2434
#接続の最大数
BACKLOG = 10
#ソケットから受信するデータのバッファサイズ
BUFSIZE = 4096

print('try socket')
#ソケットを作成する
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('try connect')
#読み込んだ音源を再生する
pygame.mixer.music.play(-1)
try:
    #作成したソケットにアドレスとポート番号を設定
    sock.bind((HOST, PORT))
    sock.listen(BACKLOG)
    while True:
    #clientからの接続を開始
        conn, address  = sock.accept()
        try:
            while True:
                #recv:ソケットからデータを受信
                b_msg = conn.recv(BUFSIZE)
                #バイトコードが送られてくるのでデコードする
                msg = b_msg.decode('utf-8')
                #受信したデータをfloat型に変更する
                laugh = float(msg)
                print(laugh)
                #laughの数値が0.9以下なら音楽を止める
                if laugh < 0.9:
                    pygame.mixer.music.pause()
                #laughの数値が0.9以上なら音源再生を再開する
                else:
                    pygame.mixer.music.unpause()
                #ソケットにデートを送信
                conn.send(b'you sent"' + b_msg + b'"')

        finally:
            #接続のクローズ
            conn.close()
finally:
    #接続のクローズ
    sock.close()


print('end')
