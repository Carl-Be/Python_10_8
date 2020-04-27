"""
Carl Bechie
CIS 185
ex 10.8
"""

from socket import *
from codecs import decode
from threading import Thread

BUFSIZE = 1024
CODE = "ascii"

class ATMClientHandler(Thread):
    """Handles ATM requests from a client."""
    
    def __init__(self, client, bank):
        """Save references to the client socket and bank."""
        Thread.__init__(self)
        self.client = client
        self.bank = bank
   
    def run(self):
        """Sends a greeting to the client, then enters
        an interative loop to take and respond to
        requests."""
        self.client.send(bytes("Welcome to the bank!",
                               CODE))
        while True:
            request = decode(self.client.recv(BUFSIZE),
                             CODE)
            if not request:
                print("Client disconnected")
                self.client.close()
                break
            else:
                reply = self.interpret(request.split())
                self.client.send(bytes(reply, CODE))

    def interpret(self, request):
        """Interprets and responds to request."""
        command = request[0]
        if command == "LOGIN":
            self.account = self.bank.get(request[1], request[2])
            if not self.account:
                return "FAILURE"
            else:
                return "SUCCESS"
        elif command == "LOGOUT":
            self.account = None
            return "Welcome to the bank!"
        elif command == "BALANCE":
            balance = self.account.getBalance()
            return "The balance is $" + str(balance)
        elif command == "DEPOSIT":
            message = self.account.deposit(float(request[1]))
            if message:
                return message
            else:
                return "Deposit successful!"
        elif command == "WITHDRAW":
            message = self.account.withdraw(float(request[1]))
            if message:
                return message
            else:
                return "Withdrawal successful!"            
        else:
            return "Command not recognized!"
            

                

