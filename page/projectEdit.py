import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import page.projectList as projectlist
import page.login as login
import page.api as api

new_user = {}
user_table = ""
roles = ["PL", "DEV", "TESTER"]
role_key = {"PL" : 0, "DEV" : 1, "TESTER" : 2}
project_id = 0

project_title = ""
title_edit = False # 기존 값과 수정되었는지 여부 
project_description = ""
description_edit = False 
origin_user = []
session = ""
username_entry = ""
role_combobox = ""

# get
def project_data(id) :
    global project_title
    global project_description
    global origin_user

    state, data = api.project_data(id, session)

    if(state) :
        project_title = data["title"]
        project_description = data["description"]
        origin_user = data["member"]
    else : 
        messagebox.showwarning("server Error", "프로젝트 데이터를 불러오는데 실패하였습니다.")

# patch
def edit_project(view) : 
    users = list(new_user.values())
    edit = {}

    if(title_edit) : 
        if not project_title:
            messagebox.showwarning("Input Error", "프로젝트 이름을 입력하세요.")
            return
        edit ["title"] = project_title
    if(description_edit) : edit["description"] = project_description
    if(len(users)>0) : edit["member"] = users
    # 수정된 것 서버에 적용

    print(edit)
    if(title_edit or description_edit or len(users)>0) :
        if(api.edit_project(edit, project_id, session)) :
            messagebox.showwarning("project edit", "프로젝트가 정상적으로 수정되었습니다.")
        else :
            messagebox.showwarning("project edit", "프로젝트 수정에 문제가 발생하였습니다.")
    projectlist.projectlist(view, session)
    
# 프로젝트 수정 페이지 호출
def projectEdit(view, id, session_get) :
    global project_id
    global new_user
    global title_edit
    global description_edit
    global session
    
    session = session_get
    new_user = {}
    title_edit = False
    description_edit = False

    # 서버에서 데이터 가져와서 위의 global 변수에 적용
    project_id = id
    project_data(id)
    projectEditView(view)

# Get
def check_user(username) :
    return api.check_user(username, session)

def add_user():
    username = username_entry.get()
    role = role_combobox.get()
    if username and role:
        for user in origin_user :
            if(user["username"] == username) : 
                messagebox.showerror("Error", "이미 프로젝트에 등록된 유저입니다")
                return 
        for user in list(new_user.values()) :
            if(user["username"] == username) : 
                messagebox.showerror("Error", "이미 프로젝트에 등록된 유저입니다")
                return
        # 새로 입력된 유저 정보 저장
        if(check_user(username)) :
            user_id = user_table.insert('', tk.END, values=(username, role))
            new_user[user_id] = {'username' : username, 'role' : role_key[role]}
            add_delete_button(user_id)
            
            # 초기화
            username_entry.delete(0, tk.END)
            role_combobox.set('')
        else :
            messagebox.showerror("Error", "존재하지 않는 유저")

# 제목이 변경 되었음을 감지
def change_title(var) :
    global title_edit
    global project_title
    project_title = var.get()
    title_edit = True

# 설명이 변경 되었음을 감지
def change_description(description):
    global description_edit
    global project_description

    if description.edit_modified():
        project_description = description.get("1.0", "end-1c")
        description_edit = True
        
        description.edit_modified(False)

# 새로 추가된 유저 중에서 삭제
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

def back(view) :
    projectlist.projectlist(view, session)

# 로그아웃    
def logout(view) :
    api.logout(session)
    login.loginView(view, session)

def projectEditView(view) :
    global user_table
    global username_entry 
    global role_combobox 

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

    # Edit Project Title
    new_project_label = ttk.Label(main_frame, text="Edit Project", font=("Arial", 20))
    new_project_label.grid(row=0, column=0, columnspan=2, sticky='w')

    # Project Setting Frame
    project_setting_frame = ttk.LabelFrame(main_frame, text="Project Setting")
    project_setting_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')

    name_label = ttk.Label(project_setting_frame, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

    name_var = tk.StringVar()
    name_entry = ttk.Entry(project_setting_frame, textvariable=name_var)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
    name_var.set(project_title)
    name_var.trace_add("write", lambda  name, index, mode: change_title(name_var))

    description_label = ttk.Label(project_setting_frame, text="Description:")
    description_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    description_entry = tk.Text(project_setting_frame, height=4)
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
    
    description_entry.insert("1.0", project_description)
    description_entry.edit_modified(False)
    description_entry.bind("<<Modified>>", lambda event: change_description(description_entry))

    # Edit button
    edit_button = ttk.Button(main_frame, text="edit", command=lambda:edit_project(view))
    edit_button.grid(row=2, column=1, pady=10, sticky='e')

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

    add_button = ttk.Button(add_user_frame, text="Add", command=add_user)
    add_button.grid(row=0, column=4, padx=5, pady=5)

    # User Table
    columns = ("username", "role", "action")
    user_table = ttk.Treeview(view, columns=columns, height= 7, show='headings')
    user_table.heading("username", text="user name")
    user_table.heading("role", text="role")
    user_table.heading("action", text="action")
    user_table.grid(row=2, column=0, columnspan=5, pady=15, padx=20, sticky='nsew')

    # Sample data
    for user in origin_user:
        user_table.insert('', tk.END, values=(user["username"], roles[user["role"]], ""))  # 기본 데이터에는 삭제 버튼을 추가하지 않음
    user_table.bind('<Button-1>', delete_user)

    # Grid configuration
    add_user_frame.grid_columnconfigure(1, weight=1)
    project_setting_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    view.grid_columnconfigure(0, weight=1)
    view.grid_rowconfigure(1, weight=1)

