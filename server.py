import socket
from _thread import *
import sys

server = "10.202.9.115"  # The IP address for the server - Currently set to my internal ip address (192.168.1.77)
port = 5555  # The port for the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Sets up a socket using IPV4 and TCP


# The reason I'm using a try/except is in case something isn't right with server/port i.e already being used, etc
try:
    s.bind((server, port))  # Binds the server and port to the socket
except socket.error as e:
    print(str(e))

s.listen(2)  # Opens up the port and allows connections
print("Waiting for a connection, Server Started")


def read_pos(str):
    """Receives a tuple in string form and returns it in int form"""
    str = str.split(",")  # Splits the text at every comma
    return int(str[0]), int(str[1])  # Returns the recreated tuple as integers

def make_pos(tup):
    """Takes a tuple and turns it into a string to be sent to server"""
    return str(tup[0]) + "," + str(tup[1])  # Returns the string tuple in the form (xx,yy)


pos = [(0, 0), (100, 100)]  # This list is going to hold the positions of the players


def threaded_client(conn, player):
    """When a client connects to the server, """

    conn.send(str.encode(make_pos(pos[player])))  # Sends the position of the player as a string tuple
    reply = ""  # Initialises the reply variable (i.e what the client sends to the server)

    while True:  # This will continue to run while the client is connected
        try:
            data = read_pos(conn.recv(2048).decode())  # The decrypted data we're trying to receive from the client
            pos[player] = data  # Updates the position on the server based on what the client has given it

            if not data:  # If we try and fail to get some data from the client, we'll disconnect from it.
                print("Disconnected")
                break
            else:  # If we are getting information
                if player == 1:  # If the client is the 2nd player
                    reply = pos[0]  # Reply with position of 1st player
                elif player == 0:  # But if the client is the 1st player
                    reply = pos[1]  # Reply with position of 2nd player
                print("Received: {}".format(data))
                print("Sending: {}".format(make_pos(reply)))

            conn.sendall(str.encode(make_pos(reply)))  # Sends the client message back to them
        except:
            print("Couldn't get information from the client")
            break

    # When the while loop ends (through disconnected or an error)
    print("Lost Connection")
    conn.close()


currentPlayer = 0

while True:
    """Continuously looks for a connection"""
    conn, addr = s.accept()  # Accepts the connection object and the address of a client
    print("Connected to: {}".format(addr))

    start_new_thread(threaded_client, (conn, currentPlayer))  # Starts a new thread for the threaded_client function
    currentPlayer += 1