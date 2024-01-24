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

NORMAL_MESSAGE_CODE = "#83bzv"
SPLITING_CODE = "/0/"

SERVER_IP = "127.0.0.1"
PORT  = 5053
ADDR = (SERVER_IP,PORT)
FORMAT = 'utf-8'

class Server:
    def __init__(self):
        self.ServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSock.bind((ADDR))
        self.ShutDownFlag = threading.Event()
        self.Clients = []
        self.RegisterLoginClients= []
        self.client_handle_exist = {}
        self.username_client = {}

        self.client_handle_message_exist = {}
        self.RecieveNewConnection()


    def HandleNewClientRegisterLogin(self, Client, ClientAddr):
        
        client_exist_event = self.client_handle_exist[Client]
        while not self.ShutDownFlag.is_set() and not client_exist_event.is_set():
            try:
                logging.info("HandleNewClientMessage function loop started")
                MessageLength = Client.recv(DEFAULT_BYTES).decode(FORMAT)
                if MessageLength:
                    MessageLength = int(MessageLength)
                    Message = Client.recv(MessageLength).decode(FORMAT)
                    if Message:
                        MessageSplited = Message.split(SPLITING_CODE)
                        if MessageSplited[0] == REGISTER_KEY:
                            logging.info("Registred Key has been Detected")
                            self.RegisterDataCollect(MessageSplited, Client)
                        elif MessageSplited[0] == LOGIN_KEY:
                            logging.info("Login key has been Detected")
                            self.LoginDataCollect(MessageSplited, Client)
                        elif MessageSplited[0] == LOGIN_COMPLETE_KEY:
                            self.client_handle_exist[Client].set()
                            logging.info("Login completed Key recieved")
                            recv_thread = threading.Thread(target=self.HandleMessage, args=(Client,ClientAddr,), daemon=True)
                            self.client_handle_message_exist[Client] = threading.Event()
                            recv_thread.start()

                        elif MessageSplited[0] == STOP_CODE:
                            logging.info("Stop Code has been detected in the HandleNewClientRegisterLogin")
                            self.close_client(Client)
                            break
                            
                        else:   
                            logging.info("Unwanted message recieved in HandleNewClientRegisterLogin")
                    else:
                        logging.error("Error in HandleNewClientRegisterLogin")

                    
            except ConnectionResetError:
                print(f"{ClientAddr} : is Disconnected from the Server")
                logging.info(f"{ClientAddr} : is Disconnected from the Server")
                if Client in self.RegisterLoginClients:
                    self.RegisterLoginClients.remove(Client)
                Client.close()
                break
            except ConnectionAbortedError:
                print(f"{ClientAddr} : is Disconnected from the Server")
                logging.info(f"{ClientAddr} : is Disconnected from the Server")
                if Client in self.RegisterLoginClients:
                    self.RegisterLoginClients.remove(Client)
                Client.close()
                break
                    


    def HandleMessage(self, Client, ClientAddr):
        Client_handle_event = self.client_handle_message_exist[Client]
        while not self.ShutDownFlag.is_set() and not Client_handle_event.is_set():
            try:
                logging.info("HandleMessage  Func loop started")
                MessageLength = Client.recv(DEFAULT_BYTES).decode(FORMAT)
                if MessageLength:
                    MessageLength = int(MessageLength)
                    Message = Client.recv(MessageLength).decode(FORMAT)
                    if Message:
                        MessageSplited = Message.split(SPLITING_CODE)
                        if MessageSplited[0] == NORMAL_MESSAGE_CODE:
                            username = self.username_client[Client]
                            self.BroadcastMessage(MessageSplited[1], username)


                        elif MessageSplited[0] == STOP_CODE:
                            self.client_handle_message_exist[Client].set()
                            self.close_client(Client)
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
        if not self.ShutDownFlag.is_set():
            self.ServerSock.listen()
            while True:
                logging.info("RecieveNewConnection function is looking for new connections\n")
                Client, ClientAddr = self.ServerSock.accept()
                self.RegisterLoginClients.append(Client)
                print(f"{ClientAddr} : is Connected to the Server")
                logging.info(f"{ClientAddr} : is Connected from the Server")
                self.client_handle_exist[Client] = threading.Event()
                HandleMessageThread = threading.Thread(target=self.HandleNewClientRegisterLogin, args=(Client,ClientAddr), daemon=True)
                HandleMessageThread.start()

    def BroadcastMessage(self, Message, username):
        """This function broadcast the message to all of the user connected to the server"""
        Message = NORMAL_MESSAGE_CODE + SPLITING_CODE + username + SPLITING_CODE + Message
        for client in self.Clients:
            MessageLength = str(len(Message)).zfill(DEFAULT_BYTES)
            client.send(MessageLength.encode(FORMAT))
            client.send(Message.encode(FORMAT))

    def RegisterDataCollect(self,MessageSplited, Client):
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
        MessageLength = str(len(Message)).zfill(4)
        Client.send(MessageLength.encode(FORMAT))
        Client.send(Message.encode(FORMAT))

    def close_client(self, Client):
        if Client in self.Clients:
            self.Clients.remove(Client)
        if Client in self.RegisterLoginClients:
            self.RegisterLoginClients.remove(Client)
        self.client_handle_exist.pop(Client, None)
        self.client_handle_message_exist.pop(Client, None)

        Client.close()



print("[+] Server is running")
server = Server()
