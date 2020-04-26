"""
File: atmclient.py
Project 10.6
This module defines the ATMClient class, which provides a window
for bank customers to perform deposits, withdrawals, and check
balances remotely via a client.
"""

from socket import *
from codecs import decode
from breezypythongui import EasyFrame

HOST = "localhost"
PORT = 5000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024
CODE = "ascii"

class ATMClient(EasyFrame):
    """Represents an ATM window for a client.
    The window connects to the server at startup and waits for
    customers to login, then sends requests to the server.
    Does not disconnect from server at logout, but waits for
    new login request from user.
    """

    def __init__(self):
        """Initialize the frame and connect to the server."""
        EasyFrame.__init__(self, title = "ATM")
        # Create and add the widgets to the window."""
        self.nameLabel = self.addLabel(row = 0, column = 0,
                                       text = "Name")
        self.pinLabel = self.addLabel(row = 1, column = 0,
                                      text = "Pin")
        self.amountLabel = self.addLabel(row = 2, column = 0,
                                         text = "Amount")
        self.statusLabel = self.addLabel(row = 3, column = 0,
                                         text = "Status")
        self.nameField = self.addTextField(row = 0, column = 1,
                                           text = "")
        self.pinField = self.addTextField(row = 1, column = 1,
                                          text = "")
        self.amountField = self.addFloatField(row = 2, column = 1,
                                              value = 0.0)
        self.statusField = self.addTextField(row = 3, column = 1,
                                             text = "",
                                             state = "readonly")
        self.balanceButton = self.addButton(row = 0, column = 2,
                                            text = "Balance",
                                            command = self.getBalance,
                                            state = "disabled")
        self.depositButton = self.addButton(row = 1, column = 2,
                                            text = "Deposit",
                                            command = self.deposit,
                                            state = "disabled")
        self.withdrawButton = self.addButton(row = 2, column = 2,
                                             text = "Withdraw",
                                             command = self.withdraw,
                                             state = "disabled")
        self.loginButton = self.addButton(row = 3, column = 2,
                                          text = "Login",
                                          command = self.login)
        # Connect to server and confirm connection
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.connect(ADDRESS)
        reply = decode(self.server.recv(BUFSIZE), CODE)
        if reply:
            self.statusField.setText(reply)
        else:
            self.statusField.setText("Could not connect")            

    def login(self):
        """Attempts to login the customer.  If successful,
        enables the buttons, including logout."""
        name = self.nameField.getText()
        pin = self.pinField.getText()
        self.server.send(bytes("LOGIN " + name + " " + pin, CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        # Reply will be the empty string if login succeeds
        if reply == "SUCCESS":
            self.statusField.setText("Hello, " + name + "!")
            self.balanceButton["state"] = "normal"
            self.depositButton["state"] = "normal"
            self.withdrawButton["state"] = "normal"
            self.loginButton["text"] = "Logout"
            self.loginButton["command"] = self.logout
        else:
            self.statusField.setText("Name and pin not recognized!")
            
    def logout(self):
        """Logs the cusomer out, clears the fields, disables the
        buttons, and enables login."""
        self.server.send(bytes("LOGOUT", CODE))
        self.nameField.setText("")
        self.pinField.setText("")
        self.amountField.setNumber(0.0)
        self.statusField.setText("Welcome to the Bank!")
        self.balanceButton["state"] = "disabled"
        self.depositButton["state"] = "disabled"
        self.withdrawButton["state"] = "disabled"
        self.loginButton["text"] = "Login"
        self.loginButton["command"] = self.login

    def getBalance(self):
        """Displays the current balance in the status field."""
        self.server.send(bytes("BALANCE", CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        self.statusField.setText(reply)

    def deposit(self):
        """Attempts a deposit. If not successful, displays
        error message in statusfield; otherwise, announces
        success."""
        amount = self.amountField.getNumber()
        self.server.send(bytes("DEPOSIT " + str(amount), CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        self.statusField.setText(reply)
        
    def withdraw(self):
        """Attempts a withdrawal. If not successful, displays
        error message in statusfield; otherwise, announces
        success."""
        amount = self.amountField.getNumber()
        self.server.send(bytes("WITHDRAW " + str(amount), CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        self.statusField.setText(reply)
        
def main(fileName = None):
    """Creates the bank with the optional file name,
    wraps the window around it, and opens the window.
    Saves the bank when the window closes."""
    ATMClient().mainloop()

if __name__ == "__main__":
    main()
