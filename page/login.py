import tkinter as tk
from tkinter import messagebox

import page.projectList as projectlist
import page.signup as signup
import page.api as api

# 서버와 연결해서 로그인 할 수 있도록
def loginCheck(id, password, session) :
    return api.loginCheck(id, password, session)

# 로그인 확인
def login(view, entry_username, entry_password, session):
    username = entry_username.get()
    password = entry_password.get()

    if(username == "" or password == "") :
        return
    # 서버에서 확인
    if loginCheck(username, password, session):  # Example credentials
        projectlist.projectlist(view, session)
    else:
        messagebox.showerror("Error", "로그인 실패")

# 회원 가입 페이지로 이동
def register(view, session):
    signup.signupView(view, session)
    
def loginView(view, session):
    for widget in view.winfo_children():
        widget.destroy()

    view.title("Login")
    view.geometry("350x300")

    # Create and place the labels and entry widgets
    label_login = tk.Label(view, text="로그인", font=("Arial", 18))
    label_login.grid(row=0, column=0, columnspan=2, pady=20)

    frame = tk.Frame(view)
    frame.grid(row=1, column=0, columnspan=2, pady=10)

    label_username = tk.Label(frame, text="아이디", font=("Arial", 14))
    label_username.grid(row=0, column=0, padx=5, pady=10)
    entry_username = tk.Entry(frame, font=("Arial", 14))
    entry_username.grid(row=0, column=1, padx=5, pady=10)

    label_password = tk.Label(frame, text="비밀번호", font=("Arial", 14))
    label_password.grid(row=1, column=0, padx=5, pady=10)
    entry_password = tk.Entry(frame, font=("Arial", 14), show='*')
    entry_password.grid(row=1, column=1, padx=5, pady=10)

    # Create and place the buttons
    frame_buttons = tk.Frame(view)
    frame_buttons.grid(row=2, column=0, columnspan=2, pady=20)

    button_login = tk.Button(frame_buttons, text="로그인", font=("Arial", 14), command=lambda: login(view, entry_username, entry_password, session))
    button_login.grid(row=0, column=0, padx=10)

    button_register = tk.Button(frame_buttons, text="회원가입", font=("Arial", 14), command=lambda: register(view, session))
    button_register.grid(row=0, column=1, padx=10)