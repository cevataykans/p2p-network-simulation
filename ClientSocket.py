import socket
import threading

from constants import BASE_PORT
from time import sleep


class ClientSocket:

    def __init__(self, ip_to_listen, peer_id, peers):
        self.ip_to_listen = ip_to_listen
        self.peer_id = peer_id
        self.sockets = []

        self.t = threading.Thread(target=self.setup, args=(peers,))
        # sleep(60)
        self.t.start()
    
    def setup(self, peers):
        for peer in peers:
            print('client socket my id =', self.peer_id, 'step ->', peer)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(True)
            cnt = 0
            while True:
                try:
                    s.connect((self.ip_to_listen, peer + BASE_PORT))
                    break
                except Exception as e:
                    if cnt < 5:
                        cnt += 1
                        print(e)
                    # print('trying to connect to ', peer)
                    pass
            print('end while')

            s.sendall(bytes(str(self.peer_id), 'utf-8'))

            self.sockets.append(s)