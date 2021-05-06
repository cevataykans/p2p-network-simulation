from constants import IN, OUT

class Graph:

    def __init__(self, filename, peer_id):
        self.peer_count = 0
        self.graph = {IN: {}, OUT: {}}
        self.peer_id = peer_id

        self.read_topology(filename)

    def read_topology(self, filename):
        with open(filename) as f:
            graph_str = f.read()
            lines = graph_str.split('\n')

            self.peer_count = int(lines[0])

            for line in lines[1: -1]:
                nodes = line.split('->')

                if nodes[0] not in self.graph[OUT]:
                    self.graph[OUT][nodes[0]] = []

                self.graph[OUT][nodes[0]].append(int(nodes[1]))

                if nodes[1] not in self.graph[IN]:
                    self.graph[IN][nodes[1]] = []

                self.graph[IN][nodes[1]].append(int(nodes[0]))
            
            print(self.graph)
    
    def get_out_peer_ids(self):
        return self.graph[OUT][self.peer_id]

    def get_in_peer_ids(self):
        return self.graph[IN][self.peer_id]