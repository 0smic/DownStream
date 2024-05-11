# Copyright (c) 2023 Gokul B
# Distributed under the MIT/X11 software license, see the accompanying
# http://www.opensource.org/licenses/mit-license.php.


import threading
import socket
from main import saveindatabase
from main import mainfunc
import logging

logging.basicConfig(filename="app_log.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

SUCCESS = 0
FAILED = 1
INVALID = 2

REGISTER_KEY = "343838459345793840193901834198384"
REGISTER_SUCCESS_KEY = "382349823790234983479143014014038"
REGISTER_FAILED_KEY = "384923452983458209452093458343984"
LOGIN_KEY = "389834934589347859429343845348528"
LOGIN_SUCCESS_KEY = "389232983294982304029834293832423"
LOGIN_FAILED_KEY = "382384283492384091234938401234813"
LOGIN_COMPLETE_KEY = "32832937498234098234901834328421"


DEFAULT_BYTES = 6

STOP_CODE = "3239341023940943523452345245234523"

SERVER_MESSAGE_CODE = "#43FN34n"
KICK_CODE = "323423439823HFD8F9834H33239U234JG3"
BAN_CODE = "34IO34344HJKDF99ADFGUFJNKNDFA9ASFF"

NORMAL_MESSAGE_CODE = "#83bzv"  # This code help to identify the normal message send by the client
SPLITING_CODE = "/0/"  #  This code used split message code and the message

SERVER_IP = "127.0.0.1"
PORT  = 5053
ADDR = (SERVER_IP,PORT)
FORMAT = 'utf-8'

class Server:
    def __init__(self):
        self.ServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSock.bind((ADDR))
        self.ShutDownFlag = threading.Event()
        self.Clients = [] # list of client are acitve 
        self.RegisterLoginClients= [] # list of client trying to register ot login
        self.client_handle_exist = {} 
        self.username_client = {} # username of client are active client
        self.client_handle_message_exist = {}

        CommandSection = self.CommandSection(self, self.ShutDownFlag, self.ServerSock, self.Clients, self.RegisterLoginClients, self.client_handle_exist, self.username_client, self.client_handle_message_exist)
        RecieveNewConnection_thread = threading.Thread(target=self.RecieveNewConnection)
        RecieveNewConnection_thread.start()
        CommandLoop_thread = threading.Thread(target=CommandSection.CommandLoop)
        CommandLoop_thread.start()
        RecieveNewConnection_thread.join()



#################-----COMMAND SECTION --------################
        
    class CommandSection:
        """This class include all the function realted to server command"""
        def __init__(self,Serverinstance, ShutDownFlag, ServerSock, Clients, RegisterLoginClients, client_handle_exist,username_client, client_handle_message_exist) -> None:
            self.Serverinstance = Serverinstance
            self.ShutDownFlag = ShutDownFlag
            self.ServerSock = ServerSock
            self.Clients = Clients
            self.RegisterLoginClients = RegisterLoginClients
            self.client_handle_exist = client_handle_exist
            self.username_client = username_client
            self.client_handle_message_exist = client_handle_message_exist

        def CommandLoop(self):
            """This func create a commandline interface in the terminal, so you can control the server by commands"""
            print("Try 'help'")
            while not self.ShutDownFlag.is_set():
                command = input(">>> ")
                splited_command = command.split(' ')
                if splited_command[0] == "help":
                    print("kick <username>    -     Kick a user from the chat for sometime")
                    print("ban <username>     -     Ban a user from the server for ever")
                    print("countuser          -     Shows no. of users are active")
                    print("lsuser             -     Shows the username of user which are active")
                    print("shutdown           -     It will shutdown the Server")
                    print("help               -     To see the commands")
                elif splited_command[0] == "shutdown":
                    self.shutdown()
                    break
                elif splited_command[0] == "countuser":
                    self.countuser()
                elif splited_command[0] == "lsuser":
                    self.lsuser()
                elif splited_command[0] == "kick":
                    self.kickout(splited_command[1])
                else:
                    print("Invalid command")

        def shutdown(self):
                """This func clear all the connections and thread of the active users and shutdown the server"""
                print("Shuting down the server...")

                for client in self.RegisterLoginClients:
                    self.RegisterLoginClients.remove(client)

                for client in self.Clients:
                    self.Clients.remove(client)

                for client in self.client_handle_exist:
                    self.client_handle_exist[client].set()
                self.client_handle_exist.clear()

                for client in self.client_handle_message_exist:
                    self.client_handle_message_exist[client].set()
                self.client_handle_message_exist.clear()
                
                print(self.username_client)
                self.username_client.clear()
                print(self.username_client)
                

                self.ShutDownFlag.set()
                self.ServerSock.close()

        def countuser(self):
            activecount = 0
            nonloginuser = 0
            for client in self.client_handle_message_exist:
                activecount = activecount + 1

            for client in self.RegisterLoginClients:
                nonloginuser = nonloginuser + 1
            print('\n')
            print(f"Pending Users in the Login/Register section :    {nonloginuser}")
            print(f"Active Users in Chat                        :    {activecount}")
            print('\n')

        def lsuser(self):
            print('\n')
            print("List of Active User's username")
            print("     --------------")
            for client, username in self.username_client.items():
                print("\t")
                print(username)

        def kickout(self, username):
            for conn, usrname in self.username_client.items():
                if usrname == username:
                    client = conn
            Message = SERVER_MESSAGE_CODE + SPLITING_CODE + KICK_CODE
            self.Serverinstance.SentToSpecificCleint(client, Message)


#################-----END OF COMMAND SECTION --------################


    def HandleNewClientRegisterLogin(self, Client, ClientAddr):
        """
        This func starts a data recveing thread when a client connected to the server.
        Also identify the credentials send by the client for login and register.
        """
        
        client_exist_event = self.client_handle_exist[Client]
        while not self.ShutDownFlag.is_set() and not client_exist_event.is_set():
            try:
                logging.info("HandleNewClientMessage function loop started")
                MessageLength = Client.recv(DEFAULT_BYTES).decode(FORMAT)  # data recv thread 
                if MessageLength:
                    MessageLength = int(MessageLength)
                    Message = Client.recv(MessageLength).decode(FORMAT)
                    if Message:
                        MessageSplited = Message.split(SPLITING_CODE)
                        if MessageSplited[0] == REGISTER_KEY:  # Register process 
                            logging.info("Registred Key has been Detected")
                            self.RegisterDataCollect(MessageSplited, Client)  # credentials for register send to the RegisterDataCollect func
                        elif MessageSplited[0] == LOGIN_KEY:  # Login Process
                            logging.info("Login key has been Detected")
                            self.LoginDataCollect(MessageSplited, Client) # Login credentials send to the LoginDataCollect func

                        elif MessageSplited[0] == LOGIN_COMPLETE_KEY: # login has been completed 
                            self.client_handle_exist[Client].set()
                            logging.info("Login completed Key recieved")
                            self.RegisterLoginClients.remove(Client)
                            recv_thread = threading.Thread(target=self.HandleMessage, args=(Client,ClientAddr,), daemon=True) 
                            self.client_handle_message_exist[Client] = threading.Event() 
                            recv_thread.start() # Started Normal Message recv thread for chatting
                        elif MessageSplited[0] == STOP_CODE: # Client has shutdown the application before login or register
                            logging.info("Stop Code has been detected in the HandleNewClientRegisterLogin")
                            self.close_client(Client) # closing all threads of that client
                            break    
                        else:   
                            logging.info("Unwanted message recieved in HandleNewClientRegisterLogin")
                    else:
                        logging.error("Error in HandleNewClientRegisterLogin")
       
            except ConnectionResetError:
                print(f"{ClientAddr} : is Disconnected from the Server")
                logging.info(f"{ClientAddr} : is Disconnected from the Server")
                self.close_client(Client)
                break
            except ConnectionAbortedError:
                print(f"{ClientAddr} : is Disconnected from the Server")
                logging.info(f"{ClientAddr} : is Disconnected from the Server")
                self.close_client(Client)
                break
                    


    def HandleMessage(self, Client, ClientAddr):
        Client_handle_event = self.client_handle_message_exist[Client]
        while not self.ShutDownFlag.is_set() and not Client_handle_event.is_set():
            try:
                logging.info("HandleMessage  Func loop started")
                MessageLength = Client.recv(DEFAULT_BYTES).decode(FORMAT) # Waiting to the message length to recv
                if MessageLength:
                    MessageLength = int(MessageLength)
                    Message = Client.recv(MessageLength).decode(FORMAT) # Waiting for the normal message to recv
                    if Message:
                        MessageSplited = Message.split(SPLITING_CODE)
                        if MessageSplited[0] == NORMAL_MESSAGE_CODE: # checking if the message is valid or a interrupted message
                            username = self.username_client[Client]
                            self.BroadcastMessage(MessageSplited[1], username)


                        elif MessageSplited[0] == STOP_CODE: # client has shutdown the application after login
                            self.client_handle_message_exist[Client].set()
                            self.close_client(Client) # closing all the threads used for that user
                            break

            except ConnectionResetError:
                print(f"{ClientAddr} : is Disconnected from the Server")
                logging.info(f"{ClientAddr} : is Disconnected from the Server")
                self.close_client(Client)
                break
            except ConnectionAbortedError:
                print(f"{ClientAddr} : is Disconnected from the Server")
                logging.info(f"{ClientAddr} : is Disconnected from the Server")
                self.close_client(Client)
                break     

    def RecieveNewConnection(self):
        """This function look for new connection and accept the connection and start a new message recieving thread and add the user in the users list"""
        print(self.ShutDownFlag)
        if not self.ShutDownFlag.is_set():
            self.ServerSock.listen()
        while not self.ShutDownFlag.is_set():
            logging.info("RecieveNewConnection function is looking for new connections\n")
            try:
                Client, ClientAddr = self.ServerSock.accept()
            except socket.error:
                if self.ShutDownFlag.is_set():
                    logging.info("Server is Shutdown by Admin")
                    break
                else:
                    logging.error("Unexpected Error Occured")

                
            self.RegisterLoginClients.append(Client)
            print(f"{ClientAddr} : is Connected to the Server")
            logging.info(f"{ClientAddr} : is Connected from the Server")
            self.client_handle_exist[Client] = threading.Event()
            HandleMessageThread = threading.Thread(target=self.HandleNewClientRegisterLogin, args=(Client,ClientAddr), daemon=True)
            HandleMessageThread.start() # Register and login credential recv thread has started for new user 
        

    def BroadcastMessage(self, Message, username):
        """This function broadcast the message to all of the user connected to the server"""
        Message = NORMAL_MESSAGE_CODE + SPLITING_CODE + username + SPLITING_CODE + Message
        for client in self.Clients:
            MessageLength = str(len(Message)).zfill(DEFAULT_BYTES)
            client.send(MessageLength.encode(FORMAT))
            client.send(Message.encode(FORMAT))

    def RegisterDataCollect(self,MessageSplited, Client):
        """This func recv all the credendital for  registeration send by the client
         and send that all data to  saveindatabase.register_data func in the main.py"""
        fields = ["username", "name","password", "email", "dob"]
        person = []
        for i in range(1,6):
            person.append(MessageSplited[i])
        username, name, password, email, dob = person
        logging.info("Data are collected RegisterDataCollect Func")
        CheckRegister = saveindatabase.register_data(username, name, password, email, dob)
        logging.info("Person data is given to the saveindatabase.register_data func")
        if CheckRegister == SUCCESS:
            logging.info("Registration Success")
            self.SentToSpecificCleint(Client, REGISTER_SUCCESS_KEY)
            logging.info("REGISTER_SUCCESS_KEY Send to the Client")
        elif CheckRegister == FAILED:
            logging.info("Registration Failed")
            self.SentToSpecificCleint(Client, REGISTER_FAILED_KEY)
            logging.info("REGISTER_FAILED_KEY Send to the Client")
        else:
            pass

    def LoginDataCollect(self, MessageSplited, Client):
        """This func recv all the credendital for login send by the client
         and send that all data to mainfunc.check_login func in the main.py"""
        fields = ["username", "password"]
        person = []
        for i in range(1,3):
            person.append(MessageSplited[i])
        username, password = person
        logging.info("Data are Collected from LoginDataCollect Func")
        check_Login = mainfunc.check_login(username, password)
        if check_Login == SUCCESS:
            logging.info("Logging Success")
            self.SentToSpecificCleint(Client, LOGIN_SUCCESS_KEY)
            logging.info('LOGIN_SUCCESS_KEY has send to the client')
            self.username_client[Client] = username
            self.Clients.append(Client)
        if check_Login == FAILED:
            logging.info("Logging failed")
            self.SentToSpecificCleint(Client, LOGIN_FAILED_KEY)
            logging.info('LOGIN_FAILED_KEY has send to the client')
        else:
            pass




    def SentToSpecificCleint(self, Client, Message):
        """This func used to send message to specific client"""
        MessageLength = str(len(Message)).zfill(DEFAULT_BYTES)
        Client.send(MessageLength.encode(FORMAT))
        Client.send(Message.encode(FORMAT))

    def close_client(self, Client):
        """This func close all the thread of all client"""
        if Client in self.Clients:
            self.Clients.remove(Client)
        if Client in self.RegisterLoginClients:
            self.RegisterLoginClients.remove(Client)
        self.client_handle_exist.pop(Client, None)
        self.client_handle_message_exist.pop(Client, None)
        Client.close()



print("[+] Server is running")
server = Server()
