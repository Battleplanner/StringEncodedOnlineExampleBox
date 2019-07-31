import socket


class Network:
    """A class that is responsible for connecting to the server"""
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a socket object
        self.server = "10.202.9.115"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()  # Connect to the server and collect the data from it

    def getPos(self):
        return self.pos

    def connect(self):

        try:
            self.client.connect(self.addr)  # Try and connect the socket object to the server
            return self.client.recv(2048).decode()  # Receives data from the server
        except:
            print("Attempt at connecting to server has failed")
            pass

    def send(self, data):
        """Responsible for sending data to the server"""
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()  # Gets response from the server
        except socket.error as e:
            print(e)