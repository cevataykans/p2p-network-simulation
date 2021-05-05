import socket
import base64
import time
import sys
import threading

BASE_PORT = 60000
graph = {}
n = 0


def read_topology():
    with open('topology.txt') as f:
        graph_str = f.read()
        lines = graph_str.split('\n')

        global n
        n = int(lines[0])
        print(n)

        global graph
        for line in lines[1: -1]:
            nodes = line.split('->')
            print(nodes)

            if nodes[0] not in graph:
                graph[nodes[0]] = []

            graph[nodes[0]].append(nodes[1])
        
        print(graph)


def get_clients(ip_address, process_id):
    # server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 100000)
        print('##### ', ip_address, process_id)
        s.bind((ip_address, process_id + BASE_PORT))
        global n
        s.listen(n)

        client_connection = None
        client_address = None
        # while True:
        client_connection, client_address = s.accept()
        
        while True:
            req = client_connection.recv(1024).decode()

            print('a', req)

            # if req is not '':
            #     print(req)


def sendAndReceiveResponse(socket, request, my_bytes=1024):
    socket.sendall(bytes(request, 'utf-8'))
    # data = socket.recv(my_bytes + 500)
    # data = data.decode('utf-8')
    # return data


def connect_to_servers(ip_address, process_id):
    # client socket
    for neighbor_id in graph[str(process_id)]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                s.connect((ip_address, int(neighbor_id) + BASE_PORT))
                break
            except:
                pass

        req = 'GET / HTTP/1.1\r\n'
        req += 'Host: localhost:8000\r\n\r\n'

        sendAndReceiveResponse(s, req)
        # print('b', response)
        # s.send(data)


def setup_network(ip_address, process_id):
    t1 = threading.Thread(target=get_clients, args=(ip_address, process_id))
    t2 = threading.Thread(target=connect_to_servers, args=(ip_address, process_id))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    ip_address = sys.argv[1]
    process_id = int(sys.argv[2])

    read_topology()

    setup_network(ip_address, process_id)