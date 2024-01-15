from typing import Optional, Tuple, Union
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk

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
        self.login = customtkinter.CTkButton(self, text="Login", command=self.login)
        self.login.grid(row=2, column=0, pady=(5, 100), sticky="")

        # Configure row and column weights for centering
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def register(self):
        print("register test")

    def switch_to_register(self):
        # Call the callback to switch to the Register frame
        self.switch_frame_callback("RegisterFrame")

    def login(self):
        print("login test")

class RegisterFrame(customtkinter.CTkFrame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback

        # Back to the main frame button
        back_image = Image.open("back-icon.png")
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



        self.email_label = customtkinter.CTkLabel(self, text="Date of Birth:")
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
        
        
    def switch_to_main(self):
        # Call the callback to switch back to the main frame
        self.switch_frame_callback("FirstSectionFrame")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
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

    def show_frame(self, frame_name):
        # Destroy the current frame (if any)
        if self.current_frame:
            self.current_frame.destroy()

        # Switch to the specified frame
        if frame_name == "FirstSectionFrame":
            self.current_frame = FirstSectionFrame(self, self.show_frame)
        elif frame_name == "RegisterFrame":
            self.current_frame = RegisterFrame(self, self.show_frame)

        self.current_frame.grid(row=0, column=0, padx=20, pady=60, sticky="nsew")

app = App()
app.mainloop()