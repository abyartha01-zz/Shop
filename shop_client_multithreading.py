#Customer as a client
import socket
from os import system, name

#To clear screen
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


#Main function
mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
host = socket.gethostname()
port = 12345

mainSocket.connect((host, port))

choice = "Y"

while choice == "Y":
    clear()

    order = input("\nEnter the item you want to order and its quantity (name, qty): ")
    mainSocket.send(order.encode())

    rcv = mainSocket.recv(1024).decode()

    print("\nMessage received from shop: ", rcv)

    if rcv == "Transaction successfull.":
        rcv = mainSocket.recv(1024).decode()

        print("\nNo. of buyers who bought your item: ", rcv, sep = "")

    choice = input("\nDo you want to order again? (y/n) ").upper()

    mainSocket.send(choice.encode())

mainSocket.close()
