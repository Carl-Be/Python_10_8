"""
Carl Bechie
CIS 185
ex 10.8
"""

from socket import *
from atmclienthandler import ATMClientHandler
from bank import createBank

HOST = "localhost"
PORT = 5000
ADDRESS = (HOST, PORT)

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS)
server.listen(5)
bank = createBank(5)
print(bank)            # Show the account credentials for testing

# The server now just waits for connections from clients
# and hands sockets off to client handlers
while True:
    print("Waiting for connection . . .")
    client, address = server.accept()
    print("... connected from: ", address)
    handler = ATMClientHandler(client, bank)
    handler.start()
