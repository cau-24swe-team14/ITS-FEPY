import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import page.projectList as projectlist
from tkinter import messagebox

import page.api as api
import page.login as login

new_user = {}
user_table = None
roles = ["PL", "DEV", "TESTER"]
role_key = {"PL" : 0, "DEV" : 1, "TESTER" : 2}
session = ""

# POST
def create_project(view, name_entry, description_entry):
    project_name = name_entry.get().strip()
    project_description = description_entry.get("1.0", tk.END).strip()

    # 프로젝트 이름이 기입되는것을 강제
    if not project_name:
        messagebox.showwarning("Input Error", "프로젝트 이름을 입력하세요.")
        return

    create = {"title" : project_name, 
              "description" : project_description, 
              "member" : list(new_user.values())}
    
    if(api.create_project(create, session)) :
        messagebox.showinfo("project create", "성공적으로 프로젝트가 생성되었습니다.")
    else : 
        messagebox.showinfo("project create", "프로젝트 생성 과정에서 문제가 발생하였습니다.")
    projectlist.projectlist(view, session)

# Get
def check_user(username) :
    return api.check_user(username, session)

def add_user(username_entry, role_combobox):
    global user_table
    username = username_entry.get()
    role = role_combobox.get()
    if username and role:
        for user in new_user.values() :
            if(user["username"] == username) : 
                messagebox.showerror("Error", "이미 프로젝트에 등록된 유저입니다")
                return
        # 새로 입력된 유저 정보 저장
        if(check_user(username)) :
            user_id = user_table.insert('', tk.END, values=(username, role))
            new_user[user_id] = {'username' : username, 'role' : role_key[role]}
            add_delete_button(user_id)
            username_entry.delete(0, tk.END)
            role_combobox.set('')
        else :
            messagebox.showerror("Error", "존재하지 않는 유저")

def delete_user(event):
    try:
        region = user_table.identify('region', event.x, event.y)
        column = user_table.identify_column(event.x)
        
        user_id = user_table.selection()[0]
        if region == 'cell' and column == '#3': # edit 클릭
            user_table.delete(user_id)
            del new_user[user_id]
    except IndexError : # 잘못 클릭한 경우
        return
    
def add_delete_button(user_id):
    # 테이블의 마지막 열에 삭제 버튼 추가
    user_table.item(user_id, values=(user_table.item(user_id, 'values')[0], user_table.item(user_id, 'values')[1], 'Delete'), tags=user_id)

# 로그아웃    
def logout(view) :
    api.logout(session)
    login.loginView(view, session)

def back(view) :
    projectlist.projectlist(view, session)


def projectcreateView(view, get_session) :
    global user_table
    global new_user
    global title_edit
    global description_edit
    global session

    session = get_session

    new_user = {}
    title_edit = False
    description_edit = False

    for widget in view.winfo_children():
        widget.destroy()
    
    view.geometry("700x550")

    # 헤더 섹션
    header_frame = ttk.Frame(view)
    header_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

    # 뒤로가기 버튼
    back_button = tk.Button(view, text="back", command=lambda: back(view))
    back_button.grid(row=0, column=1, padx=10, pady=5, sticky="e")

    # 로그아웃 버튼
    logout_button = tk.Button(view, text="logout", command=lambda: logout(view))
    logout_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    # 메인 섹션
    main_frame = ttk.Frame(view)
    main_frame.grid(row=1, column=0, columnspan=3, pady=20, padx=20, sticky='nsew')

    # New Project Title
    new_project_label = ttk.Label(main_frame, text="New Project", font=("Arial", 20))
    new_project_label.grid(row=0, column=0, columnspan=2, sticky='w')

    # Project Setting Frame
    project_setting_frame = ttk.LabelFrame(main_frame, text="Project Setting")
    project_setting_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')

    name_label = ttk.Label(project_setting_frame, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
    name_entry = ttk.Entry(project_setting_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    description_label = ttk.Label(project_setting_frame, text="Description:")
    description_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    description_entry = tk.Text(project_setting_frame, height=4)
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    # Create button
    create_button = ttk.Button(main_frame, text="create", command=lambda:create_project(view, name_entry, description_entry))
    create_button.grid(row=2, column=1, pady=10, sticky='e')

    # Add User Frame
    add_user_frame = ttk.LabelFrame(main_frame, text="Add user")
    add_user_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')

    username_label = ttk.Label(add_user_frame, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
    username_entry = ttk.Entry(add_user_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    role_label = ttk.Label(add_user_frame, text="Role:")
    role_label.grid(row=0, column=2, padx=5, pady=5, sticky='e')
    role_combobox = ttk.Combobox(add_user_frame, values=roles)
    role_combobox.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

    add_button = ttk.Button(add_user_frame, text="Add", command=lambda:add_user(username_entry, role_combobox))
    add_button.grid(row=0, column=4, padx=5, pady=5)

    # User Table
    columns = ("username", "role", "action")
    user_table = ttk.Treeview(add_user_frame, columns=columns, show='headings')
    user_table.heading("username", text="user name")
    user_table.heading("role", text="role")
    user_table.heading("action", text="action")
    user_table.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='nsew')
    user_table.bind('<Button-1>', lambda event: delete_user(event))

    # Grid configuration
    add_user_frame.grid_columnconfigure(1, weight=1)
    project_setting_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    view.grid_columnconfigure(0, weight=1)
    view.grid_rowconfigure(1, weight=1)

