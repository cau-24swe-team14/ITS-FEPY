import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

import page.issueCreate as create
import page.projectList as projectlist
import page.issueDetail as issue
import page.login as login
import page.api as api

# 드롭아웃(필터링)
statuses = ['any', 'NEW', 'ASSIGNED', 'FIXED', 'RESOLVED', 'CLOSED', 'REOPENED']
IssueFilter = ["title", "description", "keyword", 
                "reporter", "manager", "assignee", "fixer", "priority", "status"]
status_key = {'NEW' : 0, 'ASSIGNED':1, 'FIXED':2, 'RESOLVED':3, 'CLOSED':4, 'REOPENED':5}
issue_num = [5, 10, 25]

issues = []
issuesFilter = []
issuesView = []

title = ""
description = ""
member_dev = []
member_pl = []
member_tester = []

issue_filter = statuses[0]
search_filter = IssueFilter[0]
page_filter = str(issue_num[1])

projectID = -1
current_page = 1
max_page = 1
page_size = 10
isTester = False
session = ""

# issuelist 페이지를 호출하기 위해 사용
def issuelist(view, project_id, session_get) :
    global session
    global projectID

    projectID = project_id
    session = session_get

    getIssueData()
    change_page(view, 1)

# GET
# 서버에서 프로젝트 리스트 가져옴
def getIssueData() :
    # 서버에서 json 가져오도록
    global  issues
    global max_page
    global isTester
    global issuesFilter

    global title
    global description
    global member_dev
    global member_pl
    global member_tester

    isTester, data = api.getIssueData(session, projectID)

    title = data["title"]
    description = data["description"]
    issues = data["issue"]
    for user in data["member"] :
        if(user["role"] == 0) :member_pl.append(user["username"])
        elif(user["role"] == 1) :member_dev.append(user["username"])
        else : member_tester.append(user["username"])
    
    if(issues==None) :issues = []
    max_page = np.ceil(len(issues)/page_size)
    issuesFilter = issues
    
# 프로젝트 생성으로 이동
def create_issue(view) :
    create.create_issueView(view, projectID, session)

# 이슈 페이지로 이동
def issueDetail(view, issue_id) :
    issue.issueDetail(view, projectID, issue_id, session)
    
# 이슈 검색
def search(view, search_entry) :
    global  issues
    global max_page
    global search_filter
    global issuesFilter

    context = search_entry.get()
    issues = api.search(projectID, context, search_filter, session)

    if(issues==None) :issues = []
    max_page = np.ceil(len(issues)/page_size)
    issuesFilter = issues
    change_page(view, 1)

# 프로젝트 행 클릭
def table_click(view, event, tree) :
    try:
        selected_item = tree.selection()[0]
        issue_id = tree.item(selected_item, "tags")[0]
        issueDetail(view, issue_id)
    except IndexError : # 잘못 클릭한 경우
        return

# 선택한 status를 기준으로 필터링
def status_filter(event, combobox, view) :
    global issuesFilter
    global max_page
    global issue_filter

    selected_status = combobox.get()
    issue_filter = selected_status

    if("any"!=selected_status):     
        issuesFilter = []
        for issue in issues : 
            if(issue["status"]==status_key[selected_status]) :
                issuesFilter.append(issue)
    else : issuesFilter = issues
    max_page = np.ceil(len(issuesFilter)/page_size)
    change_page(view, 1)

# 선택한 서치 필터를 기준으로 검색
def search_filter_func(event, combobox, view) :
    global issuesFilter
    global search_filter

    search_filter = combobox.get()

def set_page_size(event, combobox, view) :
    global page_size
    global max_page
    global page_filter

    page_size = int(combobox.get())
    page_filter = str(page_size)
    max_page = np.ceil(len(issuesFilter)/page_size)
    change_page(view, 1)

# 페이지 변경
def change_page(view, new_page) :
    global current_page
    global issuesView

    current_page = new_page
    end_issue = min(len(issuesFilter), new_page*page_size)
    issuesView = issuesFilter[(new_page-1)*page_size:end_issue]
    issuelistView(view)

# 로그아웃    
def logout(view) :
    api.logout(session)
    login.loginView(view, session)

def back(view) :
    projectlist.projectlist(view, session)
    
def project_detail(event) :
    member = ""
    if(len(member_pl)>0) :
        member += "PL-\t"
        for user in member_pl : 
            member += user+", "
        member = member[:-2]+"\n"

    if(len(member_dev)>0) :
        member += "Dev-\t"
        for user in member_dev :
            member += user+", "
        member = member[:-2]+"\n"

    if(len(member_tester)>0) :
        member += "Tester-\t"
        for user in member_tester :
            member += user+", "
        member = member[:-2]+"\n"
    
    messagebox.showwarning("info", 
                           f"Member : \n{member}\nDescription : {description}")

# 프로젝트 페이지 구성
def issuelistView(view):
    for widget in view.winfo_children():
        widget.destroy()
    
    view.title("IssueList")
    view.geometry("830x400")
    
    title_frame = tk.Frame(view)
    title_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    
    # Title
    title_label = tk.Label(title_frame, text="Issue", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, padx=2, pady=10, sticky="w")

    # ProjectName
    project_name_label = tk.Label(title_frame, text=f"/{title}", font=("Helvetica", 16))
    project_name_label.grid(row=0, column=1, padx=2, pady=10, sticky="w")
    project_name_label.bind("<Button-1>", project_detail)

    button_frame = tk.Frame(view)
    button_frame.grid(row=0, column=1, padx=10, pady=5, sticky="e")
    
    # 뒤로가기 버튼
    back_button = tk.Button(button_frame, text="back", command=lambda: back(view))
    back_button.grid(row=0, column=0, pady=5, sticky="e")

    # 로그아웃 버튼
    logout_button = tk.Button(button_frame, text="logout", command=lambda: logout(view))
    logout_button.grid(row=0, column=1, pady=5, sticky="e")

    # Search Bar
    search_frame = tk.Frame(view)
    search_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    search_label = tk.Label(search_frame, text="Search:")
    search_label.grid(row=0, column=0, padx=5)
    search_entry = tk.Entry(search_frame, width=25)
    search_entry.grid(row=1, column=0, padx=5)

    # 검색 필터
    search_combobox = ttk.Combobox(search_frame, values=IssueFilter, width=10)
    search_combobox.set(search_filter)
    search_combobox.grid(row=1, column=1, padx=5)
    search_combobox.bind('<<ComboboxSelected>>', lambda event: search_filter_func(event, status_combobox, view))

    # 검색 버튼
    search_button = tk.Button(search_frame, text="search", command=lambda: search(view, search_entry))
    search_button.grid(row=1, column=2, pady=5, sticky="w")

    # Filters dropout 
    status_label = tk.Label(search_frame, text="Status:")
    status_label.grid(row=0, column=3, padx=5)
    status_combobox = ttk.Combobox(search_frame, values=statuses, width=10)
    status_combobox.set(issue_filter)
    status_combobox.grid(row=1, column=3, padx=5)
    status_combobox.bind('<<ComboboxSelected>>', lambda event: status_filter(event, status_combobox, view))

    # num project dropout
    page_size_combobox = ttk.Combobox(search_frame, values=issue_num, width=5)
    page_size_combobox.grid(row=1, column=6, padx=5)
    page_size_combobox.set(page_filter)
    page_size_combobox.bind('<<ComboboxSelected>>', lambda event: set_page_size(event, page_size_combobox, view))
    
    if(isTester) :
        # Create Project Button
        create_project_button = tk.Button(view, text="+ Create issue", command=lambda : create_issue(view))
        create_project_button.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    # issue Table
    columns = ('Title', 'Status', 'Start date', 'Due date')
    tree = ttk.Treeview(view, columns=columns, show='headings')
    tree.heading('Title', text='Title')
    tree.heading('Status', text='Status')
    tree.heading('Start date', text='Start date')
    tree.heading('Due date', text='Due date')
    tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    for issue in issuesView :
        tree.insert('', tk.END, values=(issue["title"], statuses[issue["status"]+1], issue["reportedDate"], issue["dueDate"]), tag = (issue["id"]))

    tree.bind('<Button-1>', lambda event: table_click(view, event, tree))

    # Pagination(페이지)
    pagination_frame = tk.Frame(view)
    pagination_frame.grid(row=3, column=0, columnspan=2, pady=10)

    if(current_page>1) :
        prev_button = tk.Button(pagination_frame, text="<", command=lambda: change_page(view, current_page-1))
        prev_button.grid(row=0, column=0, padx=5)

    page_button = tk.Button(pagination_frame, text=str(current_page))
    page_button.grid(row=0, column=1, padx=2)

    if(current_page<max_page) :
        next_button = tk.Button(pagination_frame, text=">", command=lambda: change_page(view, current_page+1))
        next_button.grid(row=0, column=2, padx=5)
