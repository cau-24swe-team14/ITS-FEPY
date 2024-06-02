import tkinter as tk
from tkinter import ttk, messagebox

import page.api as api
import page.issueDetail as issuedetail
import page.login as login

IssueKeyword = ["bug", "feature", "performance", 
                "security", "ui", "db", "integration", "network", "api", "docs"]
IssuePriority = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "TRIVIAL"]

IssueKeyword_dic = {"bug" : 0, "feature" : 1, "performance" : 2, 
                "security" : 3, "ui" : 4, "db" : 5, "integration" : 6, "network" : 7, "api" : 8, "docs" : 9}
IssuePriority_dic = {"BLOCKER" : 0, "CRITICAL" : 1, "MAJOR" : 2, "MINOR" : 3, "TRIVIAL" : 4}

session = ""

title = ""
title_edit = False
description = ""
description_edit= False
keyword = IssueKeyword[0]
keyword_edit = False
priority = IssuePriority[0]
priority_edit = False
due_date = ""
due_date_edit = False

projectId = 0
issueId = 0

def priority_change(event, priority_combo) :
    global priority
    global priority_edit
    if(priority != priority_combo.get()) :
        priority_edit = True
        priority = priority_combo.get()

def keyword_change(event, keyword_combo) :
    global keyword
    global keyword_edit
    if(keyword != keyword_combo.get()) :
        keyword_edit = True
        keyword = keyword_combo.get()

def edit(view, title_entry, description_text, duedate_entry) :
    if(title_entry.get() == "") :
        messagebox.showwarning("error","이슈 제목을 입력하세요.")
        return
    
    if(duedate_entry.get() == "") :
        messagebox.showwarning("error","dueDate를 입력하세요.")
        return
    
    edit = {}
    
    if(title_edit) : edit["title"] = title_entry.get()
    if(description_edit) : edit["description"] = description_text.get("1.0", "end-1c")
    if(priority_edit) : edit["priority"] = IssuePriority_dic[priority]
    if(keyword_edit) : edit["keyword"] = IssueKeyword_dic[keyword]
    if(due_date_edit) : edit["dueDate"] = duedate_entry.get()
    
    if(api.edit_issue(projectId, issueId, edit, session)) :
        messagebox.showwarning("issue edit","이슈를 성공적으로 수정하였습니다.")
    else :
        messagebox.showwarning("issue edit","이슈 수정에 실패하였습니다.")
    issuedetail.issueDetail(view, projectId, issueId, session)

# 이슈 디테일 데이터 가져옴
def getIssue(projectId, issueId, session):
    global title
    global description
    global priority
    global keyword
    global priority
    global due_date
    
    global title_edit
    global description_edit
    global priority_edit
    global keyword_edit
    global priority_edit
    global due_date_edit

    title_edit = False
    description_edit = False
    priority_edit = False
    keyword_edit = False
    priority_edit = False
    due_date_edit = False

    data = api.getIssue(projectId, issueId, session)
    title = data["title"]
    description = data["description"]
    priority = IssuePriority[data["priority"]]
    keyword = IssueKeyword[data["keyword"]]
    due_date = data["dueDate"]
    print(due_date)

# 이벤트 리스너 _ 타이틀 변경 여부 확인
def change_title(var) :
    global title_edit
    global title
    title = var.get()
    title_edit = True

# 이벤트 리스너 _ 설명 변경 여부 확인
def change_description(var) :
    global description_edit
    global description

    if var.edit_modified():
        description = var.get("1.0", "end-1c")
        description_edit = True
        var.edit_modified(False)

# 이벤트 리스너 _ 설명 변경 여부 확인
def change_duedate(var) :
    global due_date_edit
    global due_date
    due_date = var.get()
    due_date_edit = True

# 로그아웃    
def logout(view) :
    api.logout(session)
    login.loginView(view, session)

def back(view) :
    issuedetail.issueDetail(view, projectId, issueId, session)

def edit_issueView(view, project_id, issue_id, session_get) :
    global session
    global projectId
    global issueId
    global title

    session = session_get
    projectId = project_id
    issueId = issue_id

    getIssue(projectId, issueId, session)
    for widget in view.winfo_children():
        widget.destroy()

    
    view.title("Edit Issue")
    view.geometry("600x350")

    # Edit a frame to hold the form
    frame = ttk.Frame(view, padding="10 10 10 10")
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # New Issue label
    ttk.Label(frame, text="Edit Issue", font=("Helvetica", 16)).grid(column=0, row=0, columnspan=4, sticky=(tk.W, tk.E))

    button_frame = tk.Frame(frame)
    button_frame.grid(row=0, column=1, padx=10, pady=5, sticky=(tk.E))
    
    # 뒤로가기 버튼
    back_button = tk.Button(button_frame, text="back", command=lambda: back(view))
    back_button.grid(row=0, column=0, pady=5, sticky=tk.E)

    # 로그아웃 버튼
    logout_button = tk.Button(button_frame, text="logout", command=lambda: logout(view))
    logout_button.grid(row=0, column=1, pady=5, sticky=tk.E)

    # Title label and entry
    ttk.Label(frame, text="Title:").grid(column=0, row=1, sticky=tk.W)
    title_var = tk.StringVar()
    title_entry = ttk.Entry(frame, width=40, textvariable=title_var)
    title_entry.grid(column=1, row=1, columnspan=3, sticky=(tk.W, tk.E))
    title_var.set(title)
    title_var.trace_add("write", lambda  name, index, mode: change_title(title_var))

    # Description label and text box
    ttk.Label(frame, text="Description:").grid(column=0, row=2, sticky=tk.W)
    description_text = tk.Text(frame, width=40, height=10)
    description_text.insert("1.0", description)
    description_text.edit_modified(False)
    description_text.bind("<<Modified>>", lambda event: change_description(description_text))
    description_text.grid(column=1, row=2, columnspan=3, sticky=(tk.W, tk.E))

    # Priority label and combo box
    ttk.Label(frame, text="Priority:").grid(column=0, row=3, sticky=tk.W)
    priority_combo = ttk.Combobox(frame, values=IssuePriority)
    priority_combo.grid(column=1, row=3, sticky=(tk.W, tk.E))
    priority_combo.bind('<<ComboboxSelected>>', lambda event: priority_change(event, priority_combo))
    priority_combo.set(priority)

    # Keyword label and entry
    ttk.Label(frame, text="Keyword:").grid(column=2, row=3, sticky=tk.W)
    keyword_combo = ttk.Combobox(frame, values=IssueKeyword)
    keyword_combo.grid(column=3, row=3, sticky=(tk.W, tk.E))
    keyword_combo.bind('<<ComboboxSelected>>', lambda event: keyword_change(event, keyword_combo))
    keyword_combo.set(keyword)

    # Due date label and entry
    duedate_var = tk.StringVar()
    ttk.Label(frame, text="Due date:").grid(column=0, row=4, sticky=tk.W)
    duedate_entry = ttk.Entry(frame, width=20, textvariable=duedate_var)
    duedate_entry.grid(column=1, row=4, sticky=(tk.W, tk.E))
    duedate_var.set(due_date)
    duedate_var.trace_add("write", lambda  name, index, mode: change_duedate(duedate_var))

    # 수정 버튼
    edit_button = ttk.Button(frame, text="Edit", command=lambda:edit(view, title_entry, description_text, duedate_entry))
    edit_button.grid(column=3, row=4, sticky=(tk.E))

    # Configure column and row weights
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=1)
    frame.rowconfigure(1, weight=1)

    # Add padding to all children of the frame
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
