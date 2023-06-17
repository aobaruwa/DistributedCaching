from datetime import datetime
import pickle
import socket 
import sys 

class Server():
    def __init__(self, port, num_clients=10):
        host = socket.gethostname()
        print("host name - ", host)
        self.server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        self.server_socket.bind((host, port))  # bind host address and port together
        self.storage = str(port) + ".db"
        f = open(self.storage, 'x'); f.close() # create a new empty storage
        self.num_clients=num_clients
        self.cache = {} # data store - {key: (value, timestamp), ... }

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
                self.get(client_conn, msg) # data like "key"
            elif cmd == "set":
                self.set(client_conn, msg) # data like set ["hello" "world"]
    
        
    def get(self, client_conn, msg):
        print("cache", self.cache, "msg: ", msg)
        cmd, key = msg.split(" ") # 
        print(f"fetching {key} ...")
        data = self.cache.get(key)
        if data:
            value, timestamp = data
            client_conn.send(f"Hit! {key} -> {value}".encode())
        else:
            client_conn.send(f"Miss ! {key} not in cache".encode())

    def set(self, client_conn, msg):
        print("cache" ,self.cache, "msg: ", msg)
        cmd, key, value, incoming_timestamp = msg.split(' ')
        if value.isnumeric(): 
            value = int(value)
  
        if key in self.cache:
            # compare times 
            val, store_timestamp = self.cache[key]
            if datetime.strptime(incoming_timestamp, '%H:%M:%S') > datetime.strptime(store_timestamp, '%H:%M:%S'): 
                self.cache[key] = value
                print(f"updating the value of {key} from {val} to {value}")
                # logging ...
                with open(self.storage, 'wb') as db:
                    pickle.dump(self.cache, db)
                print("cache" ,self.cache)
                client_conn.send(f"Assigned {value} to {key}".encode())
        else:
            self.cache[key] = (value, incoming_timestamp)
            print(f"setting {key} to {value}")
            with open(self.storage, 'wb') as db:
                pickle.dump(self.cache, db)
            client_conn.send(f"Assigned {value} to {key}".encode())
        
       
if __name__=="__main__":
    port_num = int(sys.argv[1])
    s = Server(port_num)
    s.recieve_messages()
    s.server_socket.close()
