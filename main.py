from cryptography.fernet import Fernet
import datetime
import h5py
import bcrypt

SUCCESS = 0
FAILED = 1

author = "Gokul"

class Main_Func:
    """
    In this class include every important function which make the register and login secure
    Like encryption, decryption, hashing password and matching the hashed password
    """
    def __init__(self):
        pass
    def encryption(self, username, password, name):  #This used to encrypt the hashed password
        key = Fernet.generate_key()
        #encoded_passw = password.encode()
        cipher_suit = Fernet(key)
        encrypted_passw = cipher_suit.encrypt(password)
        with h5py.File('user_key.h5', 'a') as file2: # This is where the key are stored in the file
            group = file2.create_group(username)
            group.attrs['name'] = name
            group.attrs['key'] = key
        return encrypted_passw

    def decryption(self, username):
        with h5py.File('user_details.h5', 'r') as file3: ## Checking if the user in registered and collecting the encrypted password
            if username in file3:
                group = file3[username]
                password = group.attrs['password']
                with h5py.File('user_key.h5', 'r') as file4: ## Checking if the user key is saved in the user_key and collecting the key
                    groups = file4[username]
                    key = groups.attrs['key']
                    cipher_suit = Fernet(key)
                    d_password = cipher_suit.decrypt(password)
                    #decoded_passw = decrypted_password.decode()
        return d_password # Returning the decoded password or the hashed password

    def hashing_pass(self, password):
        salt = bcrypt.gensalt()
        hashed_passw = bcrypt.hashpw(password.encode('utf8'), salt)
        return hashed_passw, salt


    def matching_hash(self, password, decrypted_password):
        entred_password = password.encode('utf8')
        if bcrypt.checkpw(entred_password, decrypted_password):
            return SUCCESS
        else:
            return FAILED
        
class Log_Func:
    """
    This class contain the function that are capable for the saving both registration and login log in files
    """
    def __init__(self):
        now = datetime.datetime.now()
        self.exact_time = now.strftime("%Y-%m-%d %H:%M:%S") #This value of the var is the year-month-day hour:minute:second

    def register_log(self, username):  #This function is used to save the registred log in a file
        log_entry = f"{self.exact_time} Username: {username}"
        with open('register_log.txt', 'a', encoding='utf8') as reg_log:
            reg_log.write(log_entry)

    def login_log(self, username): #Thiss function is used to save the login log in a file
        log_entry = f"{self.exact_time} Username: {username}"
        with open('login_log.txt', 'a', encoding='utf8') as loged_log:
            loged_log.write(log_entry)

class Save_In_Database:
    """
    This class is used to make the proper saving user data in the database
    """
    def register_data(self,username, name, password, email, dob):
        try:
            hashed_passw, salt = mainfunc.hashing_pass(password)
            encrypted_password = mainfunc.encryption(username, hashed_passw, name)
            with h5py.File('user_details.h5', 'a') as file:
                group = file.create_group(username)
                group.attrs['name'] = name
                group.attrs['salt'] = salt
                group.attrs['password'] = encrypted_password
                group.attrs['email'] = email
                group.attrs['dob'] = dob
                logfunc.register_log(username)
                return SUCCESS
        except:
            print("The Username is already exists!")
            return FAILED
        
mainfunc = Main_Func()
saveindatabase = Save_In_Database()
logfunc = Log_Func()
