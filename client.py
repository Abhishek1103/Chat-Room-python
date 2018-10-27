from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter.filedialog import askopenfilename
from RSAImplement import RSAImplement


def receive():

    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()
    

def send_file(filename):
    BUFFER_SIZE = 1024
    s = socket(AF_INET,SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    
    f = open(filename, 'rb')
    while True:
        l = f.read(BUFFER_SIZE)
        while(l):
            s.send(l)
            l = f.read(BUFFER_SIZE)
        if not l:
            f.close()
            s.close()
            break
    
    

def openFileDialog(event=None):
    filename = askopenfilename()
    # TODO: call runSelectedItem()
    send_file(filename)


def exchangeKeyPair(sock, username):
    rsa = RSAImplement()
    print("Generating Key-Pair")
    rsa.generateKeyPair(username)
    print("Generating Key Pair")
    BUFFER_SIZE = 1024

    public_key_file = username + "_public_key.pem"
    sock.send(bytes("#KEYPAIR", "utf8"))
    msg = sock.recv(BUFFER_SIZE).decode('utf8')
    print("Message: ", msg)
    HOST = '127.0.0.1'
    ADDR = (HOST, 5000)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(ADDR)

    BUFFER_SIZE = 1024
    f = open(public_key_file, 'rb')
    while True:
        l = f.read(BUFFER_SIZE)
        while(l):
            s.send(l)
            l = f.read(BUFFER_SIZE)
        if not l:
            f.close()
            s.close()
            break

    print("My Public Key Sent")

    flag = ""
    server_public_key_file = "server_public_key_saved.pem"
    flag = sock.recv(BUFFER_SIZE).decode('utf8')
    print("Flag Received: ", flag, "---")
    if flag == "#KEYPAIR" or flag == "#KEYPAIR#READY":
        if flag == "#KEYPAIR#READY":
            print("")
        else:
            msg = sock.recv(BUFFER_SIZE).decode('utf8')
        print("Message: ", msg)
        HOST = '127.0.0.1'
        ADDR = (HOST, 5000)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(ADDR)
        with open(server_public_key_file, 'wb') as fd:
            while True:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    fd.close()
                    s.close()
                    break
                fd.write(data)
        print("Server's public key received")
    



top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=40, width=60, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

file_dialog_button = tkinter.Button(top, text="Choose File", command=openFileDialog)
file_dialog_button.pack()

checkCmd = tkinter.IntVar()
checkCmd.set(-1)


def runSelectedItems():
    if checkCmd.get() == 0:
    	pass
        #############task to do if aes is selected############################
    elif checkCmd.get() == 1:
    	pass
    	#################task to do if des is selected########################
    else:
    	pass
        


checkBox1 = tkinter.Checkbutton(top, variable=checkCmd, onvalue=1, offvalue=0, text="AES encryption").pack()
checkBox2 = tkinter.Checkbutton(top, variable=checkCmd, onvalue=0, offvalue=1, text="DES encryption",justify='right').pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host ip: ')
PORT = input('Enter port: ')
USERNAME = input("Enter your username: ")
TCP_IP = HOST
TCP_PORT = int(PORT) + 1


if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

msg = client_socket.recv(BUFSIZ).decode("utf8")
#msg_list.insert(tkinter.END, msg)

client_socket.send(bytes(USERNAME, 'utf8'))
# TODO: Exchange key-pair
exchangeKeyPair(client_socket, USERNAME)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
