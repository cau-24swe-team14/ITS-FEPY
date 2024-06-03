import tkinter as tk
from tkinter import messagebox

import page.api as api
import page.projectList as projectlist


# 회원 가입
def signup(id, password, session) :
    # 서버와 연결하여 회원가입 처리
    return api.signup(id, password, session)

# 회원 가입 성공하면 프로젝트 창으로 이동
def register(view, entry_username, entry_password, entry_confirm_password, session):
    username = entry_username.get()
    password = entry_password.get()
    if(username == "" or password == "") :
        messagebox.showinfo("Registration", "아이디/패스워드를 입력하세요")
        return
    confirm_password = entry_confirm_password.get()
    if password == confirm_password:
        if(signup(username, password, session)) :
            messagebox.showinfo("Registration", "Registration Successful")
            projectlist.projectlist(view, session)
        else :
            messagebox.showinfo("Registration", "회원가입 실패")
    else:
        messagebox.showerror("Error", "패스워드 확인이 일치하지 않음")

# 회원가입창 구성
def signupView(view, session):
    for widget in view.winfo_children():
        widget.destroy()

    view.title("회원가입")
    view.geometry("400x300")

    # Create and place the labels and entry widgets
    label_register = tk.Label(view, text="회원가입", font=("Arial", 18))
    label_register.grid(row=0, column=0, columnspan=2, pady=20)

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

    label_confirm_password = tk.Label(frame, text="비밀번호 확인", font=("Arial", 14))
    label_confirm_password.grid(row=2, column=0, padx=5, pady=10)
    entry_confirm_password = tk.Entry(frame, font=("Arial", 14), show='*')
    entry_confirm_password.grid(row=2, column=1, padx=5, pady=10)

    # Create and place the buttons
    button_register = tk.Button(view, text="회원가입", font=("Arial", 14), command=lambda :register(view, entry_username, entry_password, entry_confirm_password, session))
    button_register.grid(row=3, column=0, columnspan=2, pady=20)

