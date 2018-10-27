from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter.filedialog import askopenfilename


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
    send_file(filename)


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
checkBox1 = tkinter.Checkbutton(top, variable=checkCmd, onvalue=0, offvalue=1, text="DES encryption",justify='right').pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
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

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
