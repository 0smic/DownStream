import threading
import socket
import logging

logging.basicConfig(filename="app_log.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

SUCCESS = 0
FAILED = 1
INVALID = 2
WORKING = 0
NOT_WORKING = 1

REGISTER_KEY = "343838459345793840193901834198384"
REGISTER_SUCCESS_KEY = "382349823790234983479143014014038"
REGISTER_FAILED_KEY = "384923452983458209452093458343984"
LOGIN_KEY = "389834934589347859429343845348528"
LOGIN_SUCCESS_KEY = "389232983294982304029834293832423"
LOGIN_FAILED_KEY = "382384283492384091234938401234813"

STOP_CODE = "3239341023940943523452345245234523"

LOGIN_COMPLETE_KEY = "32832937498234098234901834328421"
NORMAL_MESSAGE_CODE = "#83bzv"
SPLITING_CODE = "/0/"

SERVER_IP = "127.0.0.1"
PORT  = 5053
ADDR = (SERVER_IP,PORT)
FORMAT = 'utf-8'

DEFAULT_BYTES = 6



class Client:
    def __init__(self):
        self.ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.ClientSock.connect((ADDR))
            logging.info("Connected to Server successfully")
        except ConnectionRefusedError:
            raise ConnectionError("Failed to Connect to the Server")




    def SendMessage(self, Message):
        """This function will get the lenght of the message and send it first and then send the actual message second"""
        MessageLength = str(len(Message)).zfill(DEFAULT_BYTES)
        self.ClientSock.send(MessageLength.encode(FORMAT))
        self.ClientSock.send(Message.encode(FORMAT))

    def RecieveMessage(self, on_message_recieved, ShutDownFlag):
        """This function will recieve message from the server if only the gui is done with all the functions"""
        while not ShutDownFlag.is_set():
            try:
                logging.info(" Message Recieveing function loop started")
                MessageLength = self.ClientSock.recv(DEFAULT_BYTES).decode(FORMAT)
                if MessageLength:
                    MessageLength = int(MessageLength)
                    Message = self.ClientSock.recv(MessageLength).decode(FORMAT)
                    if Message:
                        MessageSplited = Message.split(SPLITING_CODE)
                        if MessageSplited[0] == NORMAL_MESSAGE_CODE:
                            Message = f"{MessageSplited[1]}: {MessageSplited[2]}"
                            on_message_recieved(Message)
                            

            except ConnectionResetError:
                logging.exception("Disconnected from the Server: ConnectionResetError")
                break

    def RegisterDataSend(self, username, name, password, email , dob):
        person = [username, name, password, email, dob]
        encoded_data = REGISTER_KEY
        for data in person:
            encoded_data += (SPLITING_CODE + str(data))
        self.SendMessage(encoded_data)
        logging.info("Registration data are sended to the server\n")
        while True:
            MessageLength = self.ClientSock.recv(DEFAULT_BYTES).decode(FORMAT)
            if MessageLength:
                MessageLength = int(MessageLength)
                Message = self.ClientSock.recv(MessageLength).decode(FORMAT)
                if Message:
                    MessageSplited = Message.split(SPLITING_CODE)
                    if MessageSplited[0] == NORMAL_MESSAGE_CODE:
                        logging.info("Unwanted message recieve from broadcast method in the register function")
                    else:
                        if Message == REGISTER_SUCCESS_KEY:
                            logging.info("REGISTER_SUCCESS_KEY key has been Recieved")
                            return SUCCESS
                            
                        elif Message == REGISTER_FAILED_KEY:
                            logging.info("REGISTER_FAILED_KEY key has been Recieved")
                            return FAILED
                        else:
                            logging.info("Unknown Message recieved in the Register key recv method")
                            return INVALID
                        
                    
    def LoginDataSend(self, username, password):
        person = [username, password]
        encoded_data = LOGIN_KEY
        for data in person:
            encoded_data += (SPLITING_CODE + str(data))
        self.SendMessage(encoded_data)
        while True:
            MessageLength = self.ClientSock.recv(DEFAULT_BYTES).decode(FORMAT)
            if MessageLength:
                MessageLength = int(MessageLength)
                Message = self.ClientSock.recv(MessageLength).decode(FORMAT)
                if Message:
                    MessageSplited = Message.split(SPLITING_CODE)
                    if MessageSplited[0] == NORMAL_MESSAGE_CODE:
                        logging.info("Unwanted message recieve from broadcast method in the login function")
                    else:
                        if Message == LOGIN_SUCCESS_KEY:
                            logging.info("LOGIN_SUCCESS_KEY  is Recieved")
                            self.SendMessage(LOGIN_COMPLETE_KEY)
                            logging.info("LOGGING_COMPLETED_KEY has been send to the Server")
                            return SUCCESS
                        elif Message == LOGIN_FAILED_KEY:
                            logging.info("LOGIN_FAILED_KEY  is Recieved")
                            return FAILED
                        else:
                            return INVALID
                        


    def send_normal_message(self, Message):
        Message = NORMAL_MESSAGE_CODE + SPLITING_CODE + Message
        MessageLength = str(len(Message)).zfill(DEFAULT_BYTES)
        self.ClientSock.send(MessageLength.encode(FORMAT))
        self.ClientSock.send(Message.encode(FORMAT))


    def shutdown_data_send(self):
        Message = STOP_CODE
        MessageLength = str(len(Message)).zfill(DEFAULT_BYTES)
        self.ClientSock.send(MessageLength.encode(FORMAT))
        self.ClientSock.send(Message.encode(FORMAT))
        
        


            

        


