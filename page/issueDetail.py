import requests
import tkinter as tk
from tkinter import ttk

import page.api as api
import page.issueList as issuelist
import page.issueEdit as edit
import page.login as login

IssueKeyword = ["bug", "feature", "performance", 
                "security", "ui", "db", "integration", "network", "api", "docs"]

IssuePriority = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "TRIVIAL"]

IssueStatus = ["new", "assigned", "fixed", "resolved", "closed", "reopened"]

session = ""
projectId = 0
issueId = 0
status = ""

# 로그아웃    
def logout(view) :
    api.logout(session)
    login.loginView(view, session)

def back(view) :
    issuelist.issuelist(view, projectId, session)

# 이슈 디테일 데이터 가져옴
def getIssue(projectId, issueId, session):
    data = api.getIssue(projectId, issueId, session)
    return data

def issueedit(view) :
    edit.edit_issueView(view, projectId, issueId, session)

# 이따 작업하면서 수정!!!!!!!!!!!
def status_change(event, status_combobox) :
    global status
    status = status_combobox.get()

# 프로젝트 수정 페이지 호출
def issueDetail(view, get_projectId, get_issueId, get_session):
    global session
    global projectId
    global issueId

    session = get_session
    projectId = get_projectId
    issueId = get_issueId

    for widget in view.winfo_children():
        widget.destroy()
    
    data = getIssue(projectId, issueId, session)

    # Create the main window
    view.title("Issue Detail")

    # Set window size
    view.geometry("600x600")


    # Main Title
    main_title_label = tk.Label(view, text="Issue", font=("Helvetica", 20))
    main_title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")


    print(api.username)
    print(data['reporter'])
    if(api.username == data['reporter']) :
        # 편집 버튼
        edit_button = tk.Button(view, text="edit", command=lambda: issueedit(view))
        edit_button.grid(row=0, column=1, pady=5, sticky="w")

    button_frame = tk.Frame(view)
    button_frame.grid(row=0, column=1, padx=10, pady=5, sticky="e")
    
    # 뒤로가기 버튼
    back_button = tk.Button(button_frame, text="back", command=lambda: back(view))
    back_button.grid(row=0, column=0, pady=5, sticky="e")

    # 로그아웃 버튼
    logout_button = tk.Button(button_frame, text="logout", command=lambda: logout(view))
    logout_button.grid(row=0, column=1, pady=5, sticky="e")

    # Header Frame
    header_frame = tk.Frame(view, bd=2, relief="groove")
    header_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    #   Sub Title
    sub_title_label = tk.Label(header_frame, text=f"#{issueId} {data['title']}", font=("Helvetica", 16))
    sub_title_label.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

    if(data["assignee"] == None) : data["assignee"] = ""
    if(data["priority"] == None) : data["priority"] = ""
    if(data["keyword"] == None) : data["keyword"] = ""

    tk.Label(header_frame, text=f"Reporter: {data['reporter']}").grid(row=1, column=0, padx=35, pady=5, sticky="w")
    tk.Label(header_frame, text=f"Assignee: {data['assignee']}").grid(row=1, column=1, padx=35, pady=5, sticky="w")
    tk.Label(header_frame, text=f"Priority: {IssuePriority[data['priority']]}").grid(row=2, column=0, padx=35, pady=5, sticky="w")
    tk.Label(header_frame, text=f"Keyword: {IssueKeyword[data['keyword']]}").grid(row=2, column=1, padx=35, pady=5, sticky="w")

    #   Issue Description
    tk.Label(header_frame, text="Description", font=("Helvetica", 14)).grid(row=3, column=0, padx=20, pady=5, sticky="w")
    description_label = tk.Label(header_frame, text=data["description"], wraplength=500, justify="left")
    description_label.grid(row=4, column=0, columnspan=2, padx=20, pady=5, sticky="w")

    # Edit Status Frame
    status_frame = tk.Frame(view, bd=2, height=2, relief="groove")
    status_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    tk.Label(status_frame, text="Edit status", font=("Arial", 16), width=15).grid(row=0, column=0, padx=5, pady=5, sticky="w")

    tk.Label(status_frame, text="Status: ").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    status_var = tk.StringVar()
    status_combobox = ttk.Combobox(status_frame, textvariable=status_var, values=IssueStatus, state="readonly")
    status_combobox.set(IssueStatus[data["status"]])
    status_combobox.grid(row=1, column=1, padx=20, pady=5, sticky="w")
    status_combobox.bind('<<ComboboxSelected>>', lambda event: status_change(event, status_combobox))

    tk.Label(status_frame, text="Reassign: ").grid(row=1, column=2, padx=10, pady=5, sticky="w")
    reassign_entry = tk.Entry(status_frame)
    reassign_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")

    def apply_changes():
        new_status = status_var.get()
        new_assignee = reassign_entry.get()
        # Here you would call the API to apply the changes
        # api.updateIssue(projectId, issueId, new_status, new_assignee, session)
        print(f"New Status: {new_status}, New Assignee: {new_assignee}")

    apply_button = tk.Button(status_frame, text="Apply", command=apply_changes)
    apply_button.grid(row=1, column=4, padx=10, pady=5, sticky="e")

    # Comment Frame
    comment_frame = tk.Frame(view, bd=2, height=1, relief="groove")
    comment_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    tk.Label(comment_frame, text="Comment", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5, sticky="w")

    comment_text = tk.Text(comment_frame, height=3, width=60)
    comment_text.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    comment_button = tk.Button(comment_frame, text="Post")
    comment_button.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    # Comment List Frame
    comment_list_frame = tk.Frame(view, bd=2, relief="groove")
    comment_list_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    tk.Label(comment_list_frame, text="Comment List", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Set scroll bar
    listbox = tk.Listbox(comment_list_frame, height=1, width=80)
    scrollbar = tk.Scrollbar(comment_list_frame, command=listbox.yview)

    comments = data["comment"]
    for i in range(len(comments)):
        username = comments[i]["username"]
        comment = comments[i]["content"]
        date = comments[i]["date"]
        listbox.insert(i, f"user{username}: {comment}     ||{date} ")

    listbox.configure(yscrollcommand=scrollbar.set)

    listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
    scrollbar.grid(row=1, column=1, padx=10, pady=5, sticky="ns")

    # Adjust grid configuration
    for i in range(4):
        view.grid_rowconfigure(i, weight=1)
    for i in range(2):
        view.grid_columnconfigure(i, weight=1)

    for i in range(2):
        header_frame.grid_columnconfigure(i, weight=1)
        status_frame.grid_columnconfigure(i, weight=1)
        comment_frame.grid_columnconfigure(i, weight=1)
        comment_list_frame.grid_columnconfigure(i, weight=1)


