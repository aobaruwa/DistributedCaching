import datetime
import socket
from client import Client
from consistency_hashing import ConsistentHashing
from server import Server
import sys 

class Client():
    def __init__(self, ports):
        """
        Client object that talks to servers using any of the ports listed in ### ports ###
        It uses Consistency Hashing to select and retrieve messages from the distributed cache

        input : ports - List of ports for servers listening to messages.
        """
        # start all servers
        self.host = socket.gethostname()
        ports  = [33330, 33331, 33332, 33333]
        servers = [(self.host, p) for p in ports]
        
        self.ring = ConsistentHashing(servers)

        self.client_sockets = {s : self.connect2server(s) for s in servers}


    def connect2server(self, server):
        client_socket = socket.socket()
        client_socket.connect(server)
        return client_socket

    def get_time(self):
        return datetime.datetime.now().strftime('%H:%M:%S')

    def set(self, key, value):
        server = self.ring.get_node(key)
        print(f"writing data to {server} ...")
        # client_socket = socket.socket()
        # if server not in self.connected_servers:
        #     self.client_socket.connect(server)
        #     self.connected_servers.add(server)
        curr_time = self.get_time()
        msg = "set " + str(key) + " " + str(value) + " " + curr_time
        
        client_socket  = self.client_sockets[server]
        client_socket.send(msg.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        #print("connected servers", self.connected_servers)

    def get(self, key):
        server = self.ring.get_node(key)
        print(f"retrieving data from {server} ...")

        client_socket = self.client_sockets[server]
        msg = "get " + str(key)
        client_socket.send(msg.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        #print("connected servers", self.connected_servers)


