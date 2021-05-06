import socket
import threading

from constants import BASE_PORT


class ClientSocket:

    def __init__(self, ip_to_listen, peer_id, peers):
        self.ip_to_listen = ip_to_listen
        self.peer_id = peer_id
        self.sockets = []

        self.t = threading.Thread(target=self.setup, args=(peers,))
        self.t.start()
    
    def setup(self, peers):
        for peer in peers:
            # print('client socket my id =', self.peer_id, 'step ->', peer)
            s = None
            while True:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.ip_to_listen, peer + BASE_PORT))
                    break
                except:
                    s.close()

            s.sendall(bytes(str(self.peer_id), 'utf-8'))

            self.sockets.append(s)