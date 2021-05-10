import socket
import threading
import datetime

from constants import BASE_PORT, FLOD, EXIT, USER, PASS, DEF_USERNAME, DEF_PASSWORD, OK


class ClientSocket:

    def __init__(self, ip_to_listen, peer_id, peers):
        self.ip_to_listen = ip_to_listen
        self.peer_id = peer_id
        self.sockets = []
        self.lock = threading.Lock()

        self.t = threading.Thread(target=self.setup, args=(peers,))
        self.t.start()
    
    def setup(self, peers):
        for peer in peers:
            s = None
            while True:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.ip_to_listen, peer + BASE_PORT))
                    break
                except:
                    s.close()

            if self.authenticate(s, peer):
                self.sockets.append(s)
                print('TCP connection established with peer {}.'.format(peer))
                print('Authenticated to peer {}.'.format(peer))
            else:
                s.close()
    
    def authenticate(self, socket, peer):
        msg = USER + ' ' + DEF_USERNAME + '\r\n' + PASS + ' ' + DEF_PASSWORD + '\r\n'
        socket.sendall(bytes(msg, 'utf-8'))

        res = ''
        while True:
            res = socket.recv(1024).decode()
            if res != '':
                break

        res = res[:-2].split(' ')
        if res[0] == OK:
            return True
        
        # print('Authentication Failed:', res[1])
        return False

    def start_flood(self):
        self.t = threading.Thread(target=self.send_message)
        self.t.start()
    
    def send_message(self, msg=None):
        self.lock.acquire()
        if msg is None:
            now = datetime.datetime.now()
            timestamp = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
            msg = FLOD + ' ' + str(self.peer_id) + ' ' + timestamp + '\r\n'

        for s in self.sockets:
            s.sendall(bytes(msg, 'utf-8'))
        self.lock.release()
    
    def send_exit_message(self):
        msg = EXIT + '\r\n'
        self.send_message(msg)
    

    def close(self):
        for s in self.sockets:
            s.close()