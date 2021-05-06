import threading
import socket

from constants import BASE_PORT

class ServerSocket:

    def __init__(self, ip_to_listen, peer_id, peers):
        self.ip_to_listen = ip_to_listen
        self.peer_id = peer_id
        self.sockets = []

        self.t = threading.Thread(target=self.setup, args=(peers,))
        self.t.start()

    def setup(self, peers):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.setblocking(True)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 100000)

        s.bind((self.ip_to_listen, BASE_PORT + self.peer_id))
        s.listen(len(peers))

        client_connection = None
        client_address = None
        for i in range(len(peers)):
            # print('server socket my id =', self.peer_id, 'step ->', i)
            client_connection, client_address = s.accept()
            connected_id = client_connection.recv(1024).decode()
            # print('myid ->', self.peer_id, 'connected id ->', connected_id)

            self.sockets.append(client_connection)


    def listen():
        pass