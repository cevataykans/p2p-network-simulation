import time
import sys
import datetime

from Graph import Graph
from ClientSocket import ClientSocket
from ServerSocket import ServerSocket


class Peer:
    def __init__(self, ip_address, peer_id):
        self.ip_address = ip_address
        self.peer_id = int(peer_id)
        self.graph = Graph('topology.txt', peer_id)

        self.server_socket = ServerSocket(self.ip_address, self.peer_id, self.graph.get_in_peer_ids())
        self.client_socket = ClientSocket(self.ip_address, self.peer_id, self.graph.get_out_peer_ids())

        self.server_socket.t.join()
        self.client_socket.t.join()

        # wait until the next minute mark
        current_second = datetime.datetime.now().second
        time.sleep(60 - current_second)


if __name__ == '__main__':
    ip_address = sys.argv[1]
    process_id = sys.argv[2]

    me = Peer(ip_address, process_id)