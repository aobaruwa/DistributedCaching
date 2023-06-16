import socket 
import sys 
class Server():
    def __init__(self, port, num_clients=1):

        host = socket.gethostname()
        print("host name - ", host)
        self.server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        self.server_socket.bind((host, port))  # bind host address and port together

        self.num_clients=num_clients
        self.cache = {} # data store

    def recieve_messages(self):
        # configure how many client the server can listen simultaneously
        self.server_socket.listen(self.num_clients)
        print(f"server listening to requests ...")
        client_conn, client_address = self.server_socket.accept()  # accept new connection
        print("Connection from: " + str(client_address))

        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            msg = client_conn.recv(1024).decode()
            if not msg:
                # if data is not received break
                break
            print("New message from connected user: " + str(msg), end=", ")
            cmd, *data  = msg.split(" ") #= input(' -> ')
            if cmd == "get":
                self.get(client_conn, data[0]) # data like "key"
            elif cmd == "set":
                self.set(client_conn, data) # data like set ["hello" "world"]
        # client_conn.close()
        
    def get(self, client_conn, msg):
        key = msg
        print(f"fetching {key} ...")
        value=self.cache.get(key)
        if value:
            client_conn.send(f"Hit! {key} -> {value}".encode())
        else:
            client_conn.send(f"Miss ! {key} not in cache".encode())

    def set(self, client_conn, msg):
        key, value = msg
        if value.isnumeric(): 
            value = int(value)
        self.cache[key] = value
        print(f"setting {value} to {key}")
        client_conn.send(f"Assigned {value} to {key}".encode())
       
if __name__=="__main__":
    port_num = int(sys.argv[1])
    s = Server(port_num, 1)
    s.recieve_messages()
    s.server_socket.close()
