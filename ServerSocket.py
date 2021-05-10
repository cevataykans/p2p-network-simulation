import threading
import socket

from constants import BASE_PORT, FLOD, EXIT, USER, PASS, DEF_USERNAME, DEF_PASSWORD, OK, INVALID

class ServerSocket:

    def __init__(self, ip_to_listen, peer_id, peers, client_socket):
        self.ip_to_listen = ip_to_listen
        self.peer_id = peer_id
        self.sockets = []
        self.message_table = {}
        self.client_socket = client_socket
        self.should_run = False
        self.auth_flags = {}

        self.t = threading.Thread(target=self.setup, args=(peers,))
        self.t.start()

    def setup(self, peers):
        def check_flags(socket):
            if self.auth_flags[socket][USER] and self.auth_flags[socket][PASS]:
                msg = OK + ' ' + 'Successful' + '\r\n'
                socket.sendall(bytes(msg, 'utf-8'))
                return True

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 100000)

        s.bind((self.ip_to_listen, BASE_PORT + self.peer_id))
        s.listen(len(peers))

        client_connection = None
        client_address = None
        for i in range(len(peers)):
            client_connection, client_address = s.accept()

            self.auth_flags[client_connection] = {}
            self.auth_flags[client_connection][USER] = False
            self.auth_flags[client_connection][PASS] = False

            while True:
                msg_str = client_connection.recv(1024).decode()
                if msg_str != '':
                    msg_list = msg_str.split('\r\n')[:-1]
                    # print('Received msg list:', msg_list)
                    for msg in msg_list:

                        msg_keywords = msg.split(' ')
                        
                        if msg_keywords[0] == USER:
                            if msg_keywords[1] == DEF_USERNAME:
                                self.auth_flags[client_connection][USER] = True
                                if check_flags(client_connection):
                                    self.sockets.append(client_connection)
                            else:
                                msg = INVALID + ' ' + 'Username cannot be found' + '\r\n'
                                client_connection.sendall(bytes(msg, 'utf-8'))

                        elif msg_keywords[0] == PASS:
                            if msg_keywords[1] == DEF_PASSWORD:
                                self.auth_flags[client_connection][PASS] = True
                                if check_flags(client_connection):
                                    self.sockets.append(client_connection)
                            else:
                                msg = INVALID + ' ' + 'Password is incorrect' + '\r\n'
                                client_connection.sendall(bytes(msg, 'utf-8'))
                    break

    def start_listen(self):
        self.should_run = True
        self.t = threading.Thread(target=self.listen_message)
        self.t.start()

    def listen_message(self):
        exit_counter = 0
        socket_count = len(self.sockets)
        while exit_counter < socket_count:
            for s in self.sockets:
                try:
                    msg_str = s.recv(1024).decode()
                    if msg_str != '':
                        msg_list = msg_str.split('\r\n')[:-1]
                        # print('Received msg list:', msg_list)
                        for msg in msg_list:

                            msg_keywords = msg.split(' ')

                            # print('splitted msg :', msg_keywords)

                            if msg_keywords[0] == FLOD:
                                recv_id = msg_keywords[1]
                                recv_timestamp = msg_keywords[2]
                                key = recv_id + '#' + recv_timestamp

                                if key not in self.message_table:
                                    # print('Forwarding key :', key)
                                    if recv_id != str(self.peer_id):
                                        self.client_socket.send_message(msg + '\r\n')
                                    self.message_table[key] = 0
                                
                                self.message_table[key] += 1
                            
                            elif msg_keywords[0] == EXIT:
                                exit_counter += 1
                                # print('Exit received, counter :', exit_counter, ' need :', socket_count - exit_counter)
                                if exit_counter == socket_count:
                                    break

                except Exception as e:
                    pass
    
    def close(self):
        for s in self.sockets:
            s.close()
    
    def print_table(self):
        def comparator(item):
            ss = item[1].split(':')
            val = int(ss[0]) * 60 * 60 + int(ss[1]) * 60 + int(ss[2])
            val *= 1000
            val += int(item[0])
            return val

        res = []
        for k, v in self.message_table.items():
            id, timestamp = k.split('#')
            res.append((id, timestamp, v))
        
        res.sort(key=comparator)

        print('Source Node ID \t|\t Timestamp \t|\t # of messages received')
        print('--------------------------------------------------------')

        for item in res:
            print(item[0], '\t\t|\t', item[1], '\t|\t', item[2])