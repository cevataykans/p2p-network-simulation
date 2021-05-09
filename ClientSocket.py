import socket
import threading
import datetime

from constants import BASE_PORT, FLOD, EXIT


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

    def start_flood(self):
        self.t = threading.Thread(target=self.send_message)
        self.t.start()
    
    def send_message(self, msg=None):
        if msg is None:
            now = datetime.datetime.now()
            timestamp = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
            msg = FLOD + ' ' + str(self.peer_id) + ' ' + timestamp + '\r\n'

        for s in self.sockets:
            # print('Sending message :', msg)
            s.sendall(bytes(msg, 'utf-8'))
    
    def send_exit_message(self):
        msg = EXIT + '\r\n'
        self.send_message(msg)
    

    def close(self):
        for s in self.sockets:
            s.close()