import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import page.projectList as projectlist

new_user = {}
user_table = ""
roles = ["PL", "DEV", "TESTER"]
project_id = 0

project_title = ""
title_edit = False # 기존 값과 수정되었는지 여부 
project_description = ""
description_edit = False 
origin_user = []

# get
def project_data(id) :
    global project_title
    global project_description
    global origin_user

    project_title = "title"
    project_description = "context"
    origin_user = [{"name" : "PL1", "role":"PL"}, {"name" : "PL2", "role":"PL"}, 
                   {"name" : "Dev1", "role":"Dev"}, {"name" : "Dev2", "role":"Dev"}]

# post
def edit_project(view) : 
    users = new_user.values()
    
    if(title_edit) : 
        print("title edit")
        if not project_title:
            messagebox.showwarning("Input Error", "Project name is required.")
            return
    if(description_edit) : print("description edit")
    if(len(users)>0) : print(users)
    # 수정된 것 서버에 적용

    projectlist.projectlist(view)
    
# 프로젝트 수정 페이지 호출
def projectEdit(view, id) :
    global project_id
    global new_user
    global title_edit
    global description_edit
    
    new_user = {}
    title_edit = False
    description_edit = False

    # 서버에서 데이터 가져와서 위의 global 변수에 적용
    project_id = id
    project_data(id)
    projectEditView(view)


def add_user(username_entry, role_combobox):
    username = username_entry.get()
    role = role_combobox.get()
    if username and role:
        # 새로 입력된 유저 정보 저장
        user_id = user_table.insert('', tk.END, values=(username, role))
        new_user[user_id] = {'user_id' : username, 'role' : role}
        add_delete_button(user_id)
        username_entry.delete(0, tk.END)
        role_combobox.set('')

# 제목이 변경 되었음을 감지
def change_title(var) :
    global title_edit
    global project_title
    project_title = var.get()
    title_edit = True
    print(project_title)

# 설명이 변경 되었음을 감지
def change_description(description):
    global description_edit
    global project_description

    if description.edit_modified():
        project_description = description.get("1.0", "end-1c")
        description_edit = True
        
        description.edit_modified(False)
        print(project_description)

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

def projectEditView(view) :
    global user_table

    for widget in view.winfo_children():
        widget.destroy()
    
    view.geometry("700x550")

    # 헤더 섹션
    header_frame = ttk.Frame(view)
    header_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

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

    add_button = ttk.Button(add_user_frame, text="Add", command=lambda:add_user(username_entry, role_combobox))
    add_button.grid(row=0, column=4, padx=5, pady=5)

    # User Table
    columns = ("username", "role", "action")
    user_table = ttk.Treeview(add_user_frame, columns=columns, show='headings')
    user_table.heading("username", text="user name")
    user_table.heading("role", text="role")
    user_table.heading("action", text="action")
    user_table.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='nsew')

    # Sample data
    for user in origin_user:
        user_table.insert('', tk.END, values=(user["name"], user["role"], ""))  # 기본 데이터에는 삭제 버튼을 추가하지 않음
    user_table.bind('<Button-1>', lambda event: delete_user(event))

    # Grid configuration
    add_user_frame.grid_columnconfigure(1, weight=1)
    project_setting_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    view.grid_columnconfigure(0, weight=1)
    view.grid_rowconfigure(1, weight=1)

