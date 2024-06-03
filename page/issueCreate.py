import tkinter as tk
from tkinter import ttk, messagebox

import page.api as api
import page.issueList as issuelist
import page.login as login

IssueKeyword = ["bug", "feature", "performance", 
                "security", "ui", "db", "integration", "network", "api", "docs"]
IssuePriority = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "TRIVIAL"]

IssueKeyword_dic = {"bug" : 0, "feature" : 1, "performance" : 2, 
                "security" : 3, "ui" : 4, "db" : 5, "integration" : 6, "network" : 7, "api" : 8, "docs" : 9}
IssuePriority_dic = {"BLOCKER" : 0, "CRITICAL" : 1, "MAJOR" : 2, "MINOR" : 3, "TRIVIAL" : 4}

session = ""
projectId = 0
keyword = IssueKeyword[0]
priority = IssuePriority[0]

def create_issue(view, title_entry, description_text, duedate_entry) :
    if(title_entry.get() == "") :
        messagebox.showwarning("error","이슈 제목을 입력하세요.")
        return
    
    if(duedate_entry.get() == "") :
        messagebox.showwarning("error","dueDate를 입력하세요.")
        return
    
    create = {"title" : title_entry.get(), 
              "description" : description_text.get("1.0", "end-1c"),
              "priority" : IssuePriority_dic[priority],
              "keyword" : IssueKeyword_dic[keyword],
              "dueDate" : duedate_entry.get()}
    
    if(api.create_issue(projectId, create, session)) :
        messagebox.showwarning("issue create","이슈를 성공적으로 생성하였습니다.")
    else :
        messagebox.showwarning("issue create","이슈 생성에 실패하였습니다.")
    issuelist.issuelist(view, projectId, session)

# 로그아웃    
def logout(view) :
    api.logout(session)
    login.loginView(view, session)

def back(view) :
    issuelist.issuelist(view, projectId, session)

def priority_change(event, priority_combo) :
    global priority
    priority = priority_combo.get()

def keyword_change(event, keyword_combo) :
    global keyword
    keyword = keyword_combo.get()

def create_issueView(view, project_id, session_get) :
    global session
    global projectId
    global keyword
    global priority

    session = session_get
    projectId = project_id

    keyword = IssueKeyword[0]
    priority = IssuePriority[0]

    for widget in view.winfo_children():
        widget.destroy()

    view.title("New Issue")
    view.geometry("600x350")

    # Create a frame to hold the form
    frame = ttk.Frame(view, padding="10 10 10 10")
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # New Issue label
    ttk.Label(frame, text="New Issue", font=("Helvetica", 16)).grid(column=0, row=0, columnspan=4, sticky=(tk.W, tk.E))

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
    title_entry = ttk.Entry(frame, width=40)
    title_entry.grid(column=1, row=1, columnspan=3, sticky=(tk.W, tk.E))


    # Description label and text box
    ttk.Label(frame, text="Description:").grid(column=0, row=2, sticky=tk.W)
    description_text = tk.Text(frame, width=40, height=10)
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
    ttk.Label(frame, text="Due date:").grid(column=0, row=4, sticky=tk.W)
    duedate_entry = ttk.Entry(frame, width=20)
    duedate_entry.grid(column=1, row=4, sticky=(tk.W, tk.E))

    # Create button
    create_button = ttk.Button(frame, text="Create", command=lambda:create_issue(view, title_entry, description_text, duedate_entry))
    create_button.grid(column=3, row=4, sticky=(tk.E))

    # Configure column and row weights
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=1)
    frame.rowconfigure(1, weight=1)

    # Add padding to all children of the frame
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
