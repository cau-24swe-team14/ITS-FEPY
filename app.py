import tkinter as tk
from tkinter import messagebox
import page.login as login
import sys
import requests as req

session = req.Session()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login and Signup")
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        login.loginView(self, session)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def on_closing(self):
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
