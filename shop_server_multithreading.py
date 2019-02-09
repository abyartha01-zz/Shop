#Server of a shop
import socket
import datetime
from os import system, name
import threading

#Class for the items in the shop
class items:

    def __init__(self, goods, last_purchased = "No transaction yet", no_of_buyers = 0):
        self.name = goods[0]
        self.qty = int(goods[1])
        self.last_purchased = last_purchased
        self.no_of_buyers = no_of_buyers

    def update_items(self, qty):
        self.qty -= qty
        self.last_purchased = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M %p")
        self.no_of_buyers += 1

    def display_items(self):
        print(end = "     ")
        print(self.name, self.qty, self.last_purchased, sep = "                         ")


#Class for the buyers buying from the shop
class buyers:

    def __init__(self, order, addr):
        self.order = order
        self.addr = addr

    def display_buyers(self):
        print(end = "     ")
        print(self.order[0], self.order[1], self.addr, sep = "                         ")


#To clear screen
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


#Display item list
def display_items(item_list, no_of_items):
    print("\nAvailable Items", "Available quantity", "Last purchased", sep = "               ")
    for i in range(0, no_of_items):
        item_list[i].display_items()


#Display buyers list
def display_buyers(buyer_list):
    global no_of_buyers

    print("\nOrdered Items", "Ordered quantity", "Customer (IP, Port)", sep = "               ")
    for i in range(0, no_of_buyers):
        buyer_list[i].display_buyers()


#Function to input items
def input_items():
    item_list = []

    no_of_items = int(input("\nEnter the number of items in your shop: "))

    print("\nEnter the items: (name, qty)")
    for i in range(0, no_of_items):
        print("\nItem no. ", i+1, ": ", sep = "", end = "")

        goods = tuple(input().split(", "))
        item_list.append(items(goods))

    return (no_of_items, item_list)


#Thread for client
def threaded(connectSocket, buyer_list):
    #lock.acquire()

    global no_of_buyers

    print("\nID: ", threading.current_thread().name)

    while True:
        order = tuple(connectSocket.recv(1024).decode().split(", "))

        print("\nOrder received from client with", addr, ": ", order, sep = "")

        for i in range(0, no_of_items):
            if order[0].lower() == item_list[i].name.lower():
                if item_list[i].qty == 0:
                    print("\nOrdered item is out of stock. Informing client...")
                    connectSocket.send("Ordered item is out of stock.".encode())

                elif int(order[1]) <= item_list[i].qty:
                    item_list[i].update_items(int(order[1]))

                    buyer_list.append(buyers(order, addr))
                    no_of_buyers += 1

                    clear()

                    print("\nTransaction successfull.");
                    connectSocket.send("Transaction successfull.".encode())

                    connectSocket.send(str(item_list[i].no_of_buyers).encode())

                    display_items(item_list, no_of_items)
                    display_buyers(buyer_list)

                else:
                    print("\nOrdered quantity not available. Informing client....")
                    connectSocket.send("Ordered quantity not available.".encode())

                break

        else:
            print("\nOrdered item not available. Informing client....")
            connectSocket.send("Ordered item not available.".encode())

        rcv = connectSocket.recv(1024).decode()

        if rcv != "Y":
            #lock.release()
            return


#Main function
clear()

mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
host = socket.gethostname()
port = 12345

mainSocket.bind((host, port))

(no_of_items, item_list) = input_items()

buyer_list = []
#global no_of_buyers
no_of_buyers = 0
#no_of_buyers.append(0)

clear()

display_items(item_list, no_of_items)

mainSocket.listen(5)

#lock = threading.Lock()

#connectSocket, addr = mainSocket.accept()

i = 0
t = []

while True:
    connectSocket, addr = mainSocket.accept()

    clear()

    #print("\nConnected with ", addr)

    display_items(item_list, no_of_items)

    t.append(threading.Thread(target=threaded, args=(connectSocket, buyer_list)))

    t[i].start()
    #t[i].join()

    clear()

    display_items(item_list, no_of_items)
    display_buyers(buyer_list)

    i += 1
