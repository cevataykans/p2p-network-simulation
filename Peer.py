import time
import sys
import datetime

from Graph import Graph
from ClientSocket import ClientSocket
from ServerSocket import ServerSocket
from constants import TOPOLOGY_FILE, WAIT_TIME


class Peer:
    def __init__(self, ip_address, peer_id):
        self.ip_address = ip_address
        self.peer_id = int(peer_id)
        self.graph = Graph(TOPOLOGY_FILE, peer_id)

        self.client_socket = ClientSocket(self.ip_address, self.peer_id, self.graph.get_out_peer_ids())
        self.server_socket = ServerSocket(self.ip_address, self.peer_id, self.graph.get_in_peer_ids(), self.client_socket)

        self.server_socket.t.join()
        self.client_socket.t.join()

        print('setup completed') # TODO
        
        # TODO authanticate

        # wait until the next minute mark
        current_second = datetime.datetime.now().second
        time.sleep(60 - current_second)


        # send messages
        self.server_socket.start_listen()

        for i in range(7):
            print('Step =', i)
            self.client_socket.start_flood()
            time.sleep(WAIT_TIME)

        self.client_socket.send_exit_message()
        
        self.server_socket.print_table()
        
        try:
            self.server_socket.t.join()
        except:
            pass

        self.client_socket.close()
        self.server_socket.close()


if __name__ == '__main__':
    ip_address = sys.argv[1]
    process_id = sys.argv[2]

    me = Peer(ip_address, process_id)