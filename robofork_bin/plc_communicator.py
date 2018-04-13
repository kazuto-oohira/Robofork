import sys, os, time, signal, socket, threading

# Shell起動, Background起動時もSIGINTをKeyboardInterruptで捕まえる
signal.signal(signal.SIGINT, signal.default_int_handler)

# Web's library Import
# 読み込むPythonファイルのImportがおかしいとエラーになるぞ
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from robofork_app.services.plc_service import PlcService

# コマンド引数処理
plc_server = '192.168.13.50'
plc_send_port = 0
plc_server_port = 8889
if len(sys.argv) == 2:
    plc_server = sys.argv[1]


def handle_client_connection(handled_client_socket):
    """
    受信時処理
    """
    request = handled_client_socket.recv(1024)
    print('Received {}'.format(request))

    # 受信処理
    plc_service = PlcService()
    plc_service.receive_plc_message(request)

    handled_client_socket.send('ACK')
    handled_client_socket.close()


# TCP Socket Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), plc_server_port))
server_socket.listen(1)
print('TCP Server Listening on {}:{}'.format(socket.gethostname(), plc_server_port))

# 無限ループによる接続待ち処理
while True:
    try:
        (client_socket, address) = server_socket.accept()
        print('TCP Server Accepted connection from {}:{}'.format(address[0], address[1]))

        # 別スレッドで受信時処理開始
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_socket,)
        )
        client_handler.start()

    except KeyboardInterrupt:
        # Ctrl+Cは何もせずに終了
        sys.exit()
    except:
        print("TCP Socket Server Error:", sys.exc_info()[0])
        time.sleep(5)
