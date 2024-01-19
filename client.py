import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width = False, height = False)
        self.login.configure(width = 400, height = 300)
        self.pls = Label(self.login, text = "Please Login To Continue", justify = CENTER, font = "Helvetica 14 bold")
        self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.07)
        self.labelName = Label(self.login, text = "Name", font = "Helvetica 12")
        self.labelName.place(relheight = 0.2, relx = 0.1, rely = 0.2)
        self.entryName = Entry(self.login, font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2)
        self.entryName.focus()
        self.go = Button(self.login, text = "Continue", font = "Helvetica 14 bold", command = lambda:self.goAhead(self.entryName.get()))
        self.go.place(relx = 0.4, rely = 0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        rcv = Thread(target = self.receive)
        rcv.start()

    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("Chatroom")
        self.Window.resizable(width = False, height = False)
        self.Window.configure(width = 470, height = 550, bg = "#17202A")
        self.labelHead = Label(self.Window, bg = "#17202A", fg = "#EAECEE", text = self.name, font = "Helvetica 13 bold", pady = 5)
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window, width = 450, bg = "#ABB2B9")
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)
        self.textcons = Text(self.Window, width = 20, height = 2, bg = "#17202A", fg = "#EAECEE", font = "Helvetica 14", padx = 5, pady = 5)
        self.textcons.place(relheight = 0.745, relwidth = 1, rely = 0.08)
        self.textcons.config(cursor = "arrow")
        self.labelBottom = Label(self.Window, bg = "#ABB2B9", height = 80)
        self.labelBottom.place(relwidth = 1, rely = 0.825)
        self.entryMessage = Entry(self.labelBottom, bg = "#2C3E50", fg = "#EAECEE", font = "Helvetica 13")
        self.entryMessage.place(relwidth = 0.74, relheight = 0.06, rely = 0.008, relx = 0.011)
        self.entryMessage.focus()
        self.buttonMessage = Button(self.labelBottom, text = "Send", font = "Helvetica 10 bold", width = 20, bg = "#ABB2B9", command = lambda:self.sendButton(self.entryMessage.get()))
        self.buttonMessage.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22)
        scrollbar = Scrollbar(self.textcons)
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.config(command = self.textcons.yview())

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMessage(message)
            except:
                print("An error occured!")
                client.close()
                break

    def sendButton(self, msg):
        self.textcons.config(state = DISABLED)
        self.msg = msg
        self.entryMessage.delete(0, END)
        snd = Thread(target = self.write)
        snd.start()

    def showMessage(self, message):
        self.textcons.config(state = NORMAL)
        self.textcons.insert(END, message + "\n\n")
        self.textcons.config(state = DISABLED)
        self.textcons.see(END)

    def write(self):
        self.textcons.config(state = DISABLED)
        while True:
            message = (f"{self.name}:{self.msg}")
            client.send(message.encode("utf-8"))
            self.showMessage(message)
            break

g = GUI()

#nickname = input("Choose your nickname: ")

#def receive():
#    while True:
#        try:
#            message = client.recv(2048).decode('utf-8')
#            if message == 'NICKNAME':
#                client.send(nickname.encode('utf-8'))
#           else:
#                print(message)
#        except:
#            print("An error occured!")
#            client.close()
#            break

#def write():
#    while True:
#        message = '{}: {}'.format(nickname, input(''))
#        client.send(message.encode('utf-8'))

#receive_thread = Thread(target=receive)
#receive_thread.start()
#write_thread = Thread(target=write)
#write_thread.start()