import base64
import time
import sys
import threading

from Graph import Graph
from ClientSocket import ClientSocket
from ServerSocket import ServerSocket


def setup_network(ip_address, process_id):
    t1 = threading.Thread(target=get_clients, args=(ip_address, process_id))
    t2 = threading.Thread(target=connect_to_servers, args=(ip_address, process_id))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


class Peer:
    def __init__(self, ip_address, peer_id):
        self.ip_address = ip_address
        self.peer_id = int(peer_id)
        self.graph = Graph('topology.txt', peer_id)

        # self.in_sockets = [] # push server sockets here
        # self.out_sockets = [] # push client sockets here

        self.server_socket = ServerSocket(self.ip_address, self.peer_id, self.graph.get_in_peer_ids())
        self.client_socket = ClientSocket(self.ip_address, self.peer_id, self.graph.get_out_peer_ids())

        self.server_socket.t.join()
        self.client_socket.t.join()

        # TODO wait until next minute mark


if __name__ == '__main__':
    ip_address = sys.argv[1]
    process_id = sys.argv[2]

    me = Peer(ip_address, process_id)