# Copyright (c) 2023 Gokul B
# Distributed under the MIT/X11 software license, see the accompanying
# http://www.opensource.org/licenses/mit-license.php.

from typing import Optional, Tuple, Union
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk
from client import Client
from basic_algo import SearchAlgo
import sys
import threading
from tkinter import Text, Scrollbar
import logging

logging.basicConfig(filename="app_log.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

HOST = "127.0.0.1"
PORT = 9093



SUCCESS = 0
FAILED = 1
INVAILD = 2

WORKING = 0
NOT_WORKING = 1

KICK_CODE = "323423439823HFD8F9834H33239U234JG3"
BAN_CODE = "34IO34344HJKDF99ADFGUFJNKNDFA9ASFF"


class FirstSectionFrame(customtkinter.CTkFrame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)

        self.switch_frame_callback = switch_frame_callback

        # Centered label
        self.welcome_label = customtkinter.CTkLabel(self, text="Welcome to DownStream", font=("Helvetica", 24))
        self.welcome_label.grid(row=0, column=0, columnspan=2, pady=(20, 20))

        # Register button in the center
        self.register = customtkinter.CTkButton(self, text="Register", command=self.switch_to_register)
        self.register.grid(row=1, column=0, pady=(5, 0), sticky="") 

        # Login button below the Register button, centered
        self.login = customtkinter.CTkButton(self, text="Login", command=self.switch_to_login)
        self.login.grid(row=2, column=0, pady=(5, 100), sticky="")

        # Configure row and column weights for centering
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def switch_to_register(self):
        # Call the callback to switch to the Register frame
        self.switch_frame_callback("RegisterFrame")
        logging.info("Switched to RegisterFrame")

    def switch_to_login(self):
        self.switch_frame_callback("LoginFrame")
        logging.info("Switched to LoginFrame")

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback

        # Back to the main frame button
        back_image = Image.open("rc/back-icon.png")
        back_image = back_image.resize((10,10))
        back_icon = ImageTk.PhotoImage(back_image)

        self.back_button = customtkinter.CTkButton(self, image=back_icon,text="", border_width=0, command=self.switch_to_main,fg_color="#333333",width=0)
        self.back_button.image = back_icon
        self.back_button.grid(row=0, column=0, pady=(10, 0), sticky="w")

        # Entry for the username

        self.username_label = customtkinter.CTkLabel(self, text="Username:")
        self.username_label.grid(row=3, column=0, pady=(10,0), padx=10, sticky="w")

        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.grid(row=3,column=1, pady=(10,0), padx=10, sticky="e")

        # Entry for the password
        self.password_label = customtkinter.CTkLabel(self, text="Password:")
        self.password_label.grid(row=4, column=0, pady=(10,0), padx=10, sticky="w")

        self.password_entry = customtkinter.CTkEntry(self, show="*")
        self.password_entry.grid(row=4,column=1, pady=(10,0), padx=10, sticky="e")

        # Login Button
        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login_user)
        self.login_button.grid(row=5, column=1, pady=(10,20), padx=10)


    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill all field")
        else:
            check_login = client.LoginDataSend(username , password) 
            if check_login == SUCCESS:
                self.username_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                messagebox.showinfo("Success", "You are Successfully Logged")
                logging.info("User Successfully logged In")
                self.switch_to_after_login()
            elif check_login == FAILED:
                messagebox.showerror("Error", "Wrong Password or Username")
                logging.info("Logging Failed wrong username or password")

    def switch_to_main(self):
        # Call the callback to switch back to the main frame
        self.switch_frame_callback("FirstSectionFrame")
        logging.info("Switched to MainFrame")

    def switch_to_after_login(self):
        self.switch_frame_callback("AfterLoginFrame")
        logging.info("Switched to AfterLoginFrame")


class RegisterFrame(customtkinter.CTkFrame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback

        # Back to the main frame button
        back_image = Image.open("rc/back-icon.png")
        back_image = back_image.resize((10,10))
        back_icon = ImageTk.PhotoImage(back_image)

        self.back_button = customtkinter.CTkButton(self, image=back_icon,text="", border_width=0, command=self.switch_to_main,fg_color="#333333",width=0)
        self.back_button.image = back_icon
        self.back_button.grid(row=0, column=0, pady=(10, 0), sticky="w")

        #Taking Input
        self.username_label = customtkinter.CTkLabel(self, text="Username:")
        self.username_label.grid(row=3, column=0, pady=(10, 0), padx=10, sticky="w")

        # Entry for username
        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.grid(row=3, column=1, pady=(10, 0), padx=10, sticky="e")

        self.name_label = customtkinter.CTkLabel(self, text="Name:")
        self.name_label.grid(row=4, column=0, pady=(10, 0), padx=10, sticky="w")

        # Entry for name of the User
        self.name_entry = customtkinter.CTkEntry(self)
        self.name_entry.grid(row=4, column=1, pady=(10, 0), padx=10, sticky="e")
        
        self.password_label = customtkinter.CTkLabel(self, text="Password:")
        self.password_label.grid(row=5, column=0, pady=(10, 0), padx=10, sticky="w")

        # Entry for password of the User
        self.password_entry = customtkinter.CTkEntry(self)
        self.password_entry.grid(row=5, column=1, pady=(10, 0), padx=10, sticky="e")

        self.email_label = customtkinter.CTkLabel(self, text="Email:")
        self.email_label.grid(row=6, column=0, pady=(10, 0), padx=10, sticky="w")

        # Entry for email of the User
        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="example@gmail.com")
        self.email_entry.grid(row=6, column=1, pady=(10, 0), padx=10, sticky="e")

        self.dob_label = customtkinter.CTkLabel(self, text="Date of Birth:")
        self.dob_label.grid(row=7, column=0, pady=(10, 0), padx=10, sticky="w")

        # Entry for date of birth of the User
        self.dob_entry = customtkinter.CTkEntry(self, placeholder_text="DD/MM/YY")
        self.dob_entry.grid(row=7, column=1, pady=(10, 0), padx=10, sticky="e")

        #Register Button
        self.register_button = customtkinter.CTkButton(self, text="Register", command=self.register_user)
        self.register_button.grid(row=8,column=0, pady=(10,0),padx=20, sticky="")



    def register_user(self):
        username = self.username_entry.get()
        name = self.name_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        dob = self.dob_entry.get()
        if not username or not name or not password or not email or not dob:
            messagebox.showinfo("Error", "Please fill out all the field")
            return
        else:
            check_register = client.RegisterDataSend(username, name, password, email, dob)
            print("[+] Register function completed key recieved for further implementation")
            if check_register == SUCCESS:
                self.username_entry.delete(0, 'end')
                self.name_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                self.email_entry.delete(0, 'end')
                self.dob_entry.delete(0, 'end')
                messagebox.showinfo("Sucess", "Your are Successfully Registred\n You can now login to DownStream")
                logging.info("Successfully Registred")
            elif check_register == FAILED:
                messagebox.showwarning("Failed", "This username already exists")
                logging.info("Registration Failed, Username Already Exists")
            elif check_register == INVAILD:
                messagebox.showerror("Error", "Error ocurred Try after sometime")
                logging.error("Return Invalid, Unexpected Error happened")
                
    def switch_to_main(self):
        # Call the callback to switch back to the main frame
        self.switch_frame_callback("FirstSectionFrame")
        logging.info("Switched to FirstSectionFrame")
        
class AfterLoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback
        recv_thread = threading.Thread(target=client.RecieveMessage, args=(self.on_message_recieved,ShutDownFlag,), daemon=True)
        recv_thread.start()
        app.geometry("700x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Default profile pic

        profile_image = Image.open("rc/unkown1.png")
        profile_image = profile_image.resize((20,20))
        profile_icon = ImageTk.PhotoImage(profile_image)

        ## creating a search bar

        search_image = Image.open("rc/search-icon.png")
        search_image = search_image.resize((10,10))
        search_icon = ImageTk.PhotoImage(search_image)
        
        self.search_button = customtkinter.CTkButton(self, image=search_icon, text="", width=0, command=self.search)
        self.search_button.place(relx=0.99, rely=0.02, anchor='ne')

        self.search_bar_entry = customtkinter.CTkEntry(self, placeholder_text="Search User")
        self.search_bar_entry.place(relx=0.94, rely=0.02, anchor='ne')

        self.profile_button = customtkinter.CTkButton(self, image=profile_icon, width=0, text="", fg_color="#444444")
        self.profile_button.place(relx=0.06, rely=0.02, anchor="ne")

                # Message Displaying Screen
        self.message_dis_box = customtkinter.CTkScrollableFrame(self, width=500, height=300)
        self.message_dis_box.grid(row=0, column=0, pady=(60, 0), padx=20, columnspan=2, sticky="nsew")

        # Create a Text widget and Scrollbar directly inside the frame
        self.message_display = Text(self.message_dis_box, wrap="word", state="disabled", bg="#333333", foreground="white")
        self.message_display.pack(expand=True, fill="both", side="left")

        scrollbar = Scrollbar(self.message_dis_box, command=self.message_display.yview)
        scrollbar.pack(side="right", fill="y")

        # Attach scrollbar to the Text widget
        self.message_display.config(yscrollcommand=scrollbar.set)

        # Message Entry and Send Button
        self.message_entry = customtkinter.CTkEntry(self, placeholder_text="Message")
        self.message_entry.grid(row=1, column=0, pady=(10, 10), padx=(20, 0), sticky="nsew")

        self.send_button = customtkinter.CTkButton(self, text="Send", width=20, command=self.send_normal_message)
        self.send_button.grid(row=1, column=1, pady=(10, 10), padx=(5, 20), sticky="nsew")


    def start_recieve_thread(self,  ShutDownFlag):
        client.RecieveMessage(self.on_message_recieved, ShutDownFlag)

    def on_message_recieved(self, MessageContent):
        if MessageContent == KICK_CODE:
            logging.info("ADMIN KICK YOU OUT")
            messagebox.showerror("ADMIN", "You been kicked out by the Admin")    
            app.shutdown()  
        elif MessageContent == BAN_CODE:
            logging.info("ADMIN BANNED YOU FROM THE SERVER")
            messagebox.showerror("ADMIN", "You been Banned by the Admin")    
            app.shutdown()
        else:
            self.message_display.config(state="normal")
            self.message_display.insert("end", MessageContent + "\n")
            self.message_display.see("end")
            self.message_display.config(state="disabled")
            
    def send_normal_message(self):
        message = self.message_entry.get()
        client.send_normal_message(message)
        self.message_entry.delete(0, 'end')

    def search(self):
        username = self.search_bar_entry.get()
        check_search = SearchAlgo.Search_for_user(username)
        if check_search == SUCCESS:
            print("[+] User found on the data base")
        elif check_search == FAILED:
            print(f"{username}")
            print("No user found")
    
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        logging.info("DownStream ui is Starting")
        if Connected == False:
            messagebox.showerror("Error", "Server is Offline. Come back later")
            logging.info("Server is Offline, Shuting Down the Application [+] Done")
            sys.exit()
        customtkinter.set_appearance_mode("Dark")
        self.title("DownStream")
        self.geometry("500x400")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Pass the self.show_frame as switch_frame_callback
        self.frame = FirstSectionFrame(self, self.show_frame)
        self.frame.grid(row=0, column=0, padx=20, pady=60, sticky="nsew")

        self.current_frame = None  # To keep track of the current frame
        self.show_frame("FirstSectionFrame")
        self.protocol("WM_DELETE_WINDOW",self.shutdown)

    def show_frame(self, frame_name):
        # Destroy the current frame (if any)
        if self.current_frame:
            self.current_frame.destroy()

        # Switch to the specified frame
        if frame_name == "FirstSectionFrame":
            self.current_frame = FirstSectionFrame(self, self.show_frame)
        elif frame_name == "RegisterFrame":
            self.current_frame = RegisterFrame(self, self.show_frame)
        elif frame_name == "LoginFrame":
            self.current_frame = LoginFrame(self, self.show_frame)
        elif frame_name == "AfterLoginFrame":
            self.current_frame = AfterLoginFrame(self, self.show_frame)
        self.current_frame.grid(row=0, column=0, padx=20, pady=60, sticky="nsew")


    def shutdown(self):
        ShutDownFlag.set()
        client.shutdown_data_send()
        logging.info("Shuting Down the Application [+]  Done")        
        sys.exit()


try:
    client = Client()
    Connected = True
    ShutDownFlag = threading.Event()
except ConnectionError:
    Connected = False
    

app = App()
app.mainloop()

