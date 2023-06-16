import socket
class Client():
    def __init__(self, host_port):
        host = socket.gethostname()  # as both code is running on same pc
        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((host, host_port))  # connect to the server
        msg = input("")  # take input

        while msg != "end":
            self.client_socket.send(msg.encode())  # send message
            data = self.client_socket.recv(1024).decode()  # receive response

            print('Received from server: ' + data)  # show in terminal

            msg = input("")  # again take input

        self.client_socket.close()  # close the connection
        
if __name__=="__main__":
  c = Client(host_port=30000)
