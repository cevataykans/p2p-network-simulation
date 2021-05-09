import threading
import socket

from constants import BASE_PORT, FLOD, EXIT

class ServerSocket:

    def __init__(self, ip_to_listen, peer_id, peers, client_socket):
        self.ip_to_listen = ip_to_listen
        self.peer_id = peer_id
        self.sockets = []
        self.message_table = {}
        self.client_socket = client_socket
        self.should_run = False

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

    def start_listen(self):
        self.should_run = True
        self.t = threading.Thread(target=self.listen_message)
        self.t.start()

    def listen_message(self):
        exit_counter = 0
        while exit_counter < len(self.sockets):
            for s in self.sockets:
                try:
                    msg = s.recv(1024).decode()
                    msg = msg[:-2]
                    print('Received msg :', msg)

                    if msg != '':
                        # TODO parse
                        # TODO respond to auth

                        msg_keywords = msg.split(' ')

                        print('splitted msg :', msg_keywords)

                        if msg_keywords[0] == FLOD:
                            recv_id = msg_keywords[1]
                            recv_timestamp = msg_keywords[2]
                            key = recv_id + '#' + recv_timestamp

                            if key not in self.message_table:
                                # print('Forwarding key :', key)
                                if recv_id != self.peer_id:
                                    self.client_socket.send_message(msg + '\r\n')
                                self.message_table[key] = 0
                            
                            self.message_table[key] += 1
                        
                        elif msg_keywords[0] == EXIT:
                            print('Exit received, need :', len(self.sockets))
                            exit_counter += 1
                except Exception as e:
                    print('Exception in server while listening to client :', e)
    
    def close(self):
        for s in self.sockets:
            s.close()
    
    def print_table(self):
        print(self.message_table)