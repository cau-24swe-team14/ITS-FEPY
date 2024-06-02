import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

import page.projectCraete as create
import page.projectEdit as edit
import page.issueList as issue
import page.login as login
import page.api as api

# 드롭아웃(필터링)
statuses = ['any', 'Not Started', 'In Progress', 'Done']
project_num = [5, 10, 25]

projects = []
projectsFilter = []
projectsView = []

project_filter = statuses[0]
page_filter = str(project_num[1])

current_page = 1
max_page = 1
page_size = 10
isAdmin = False
session = ""

# projectlist 페이지를 호출하기 위해 사용
def projectlist(view, session_get) :
    global isAdmin
    global projectsFilter
    global projectsView
    global session

    session = session_get

    isAdmin = getProjectData()
    projectsFilter = projects
    projectsView = projects
    change_page(view, 1)

# GET
# 서버에서 프로젝트 리스트 가져옴
def getProjectData() :
    # 서버에서 json 가져오도록
    global  projects
    global max_page

    isAdmin, projects = api.getProjectData(session)
    
    if(projects == None) : projects = []
    max_page = np.ceil(len(projects)/page_size)
    return isAdmin # Admin이면 true, 아니면 false가 들어가도록

# 이슈 리스트로 이동
def issuelist(view, project_id) :
    issue.issuelist(view, project_id, session)

# 프로젝트 수정으로 이동
def edit_project(view, project_id):
    # Functionality for editing a project
    edit.projectEdit(view, project_id, session)

# 프로젝트 생성으로 이동
def create_project(view) :
    create.projectcreateView(view, session)

# 프로젝트 행 클릭
def table_click(view, event, tree) :
    try:
        region = tree.identify('region', event.x, event.y)
        column = tree.identify_column(event.x)
        
        selected_item = tree.selection()[0]
        project_id = tree.item(selected_item, "tags")[0]
        if region == 'cell' and column == '#3': # edit 클릭
            print("edit")
            edit_project(view, project_id)
        else :
            issuelist(view, project_id)
    except IndexError : # 잘못 클릭한 경우
        return

# 선택한 status를 기준으로 필터링
def status_filter(event, combobox, view) :
    global projectsFilter
    global max_page
    global project_filter

    selected_status = combobox.get()
    project_filter = selected_status

    if("any"!=selected_status):     
        projectsFilter = []
        for project in projects : 
            if(statuses[project["status"]+1]==selected_status) :
                projectsFilter.append(project)
    else : projectsFilter = projects
    max_page = np.ceil(len(projectsFilter)/page_size)
    change_page(view, 1)

def set_page_size(event, combobox, view) :
    global page_size
    global max_page
    global page_filter

    page_size = int(combobox.get())
    page_filter = str(page_size)
    
    max_page = np.ceil(len(projectsFilter)/page_size)
    change_page(view, 1)

# 페이지 변경
def change_page(view, new_page) :
    global current_page
    global projectsView

    current_page = new_page
    end_project = min(len(projectsFilter), new_page*page_size)
    projectsView = projectsFilter[(new_page-1)*page_size:end_project]
    projectlistView(view)

# 로그아웃    
def logout(view) :
    api.logout(session)
    login.loginView(view, session)

# 프로젝트 페이지 구성
def projectlistView(view):
    for widget in view.winfo_children():
        widget.destroy()
    
    view.title("ProjectList")
    if(isAdmin):
        view.geometry("535x400")
    else :
        view.geometry("420x400")

    # Title
    title_label = tk.Label(view, text="Project", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # 로그아웃 버튼
    logout_button = tk.Button(view, text="logout", command=lambda: logout(view))
    logout_button.grid(row=0, column=1,padx=10, pady=5, sticky="e")

    # Search Bar
    search_frame = tk.Frame(view)
    search_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    
    # Filters dropout
    status_label = tk.Label(search_frame, text="Status:")
    status_label.grid(row=0, column=3, padx=5)
    status_combobox = ttk.Combobox(search_frame, values=statuses, width=10)
    status_combobox.set(project_filter)
    status_combobox.grid(row=1, column=3, padx=5)
    status_combobox.bind('<<ComboboxSelected>>', lambda event: status_filter(event, status_combobox, view))

    # num project dropout
    page_size_combobox = ttk.Combobox(search_frame, values=project_num, width=5)
    page_size_combobox.grid(row=1, column=6, padx=5)
    page_size_combobox.set(page_filter)
    page_size_combobox.bind('<<ComboboxSelected>>', lambda event: set_page_size(event, page_size_combobox, view))
    
    if(isAdmin) :
        # Create Project Button
        create_project_button = tk.Button(view, text="+ Create Project", command=lambda : create_project(view))
        create_project_button.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    # Project Table
    if(isAdmin) :
        columns = ('Title', 'Status', 'Edit')
    else :
        columns = ('Title', 'Status')
    tree = ttk.Treeview(view, columns=columns, show='headings')
    tree.heading('Title', text='Title')
    tree.heading('Status', text='Status')
    if(isAdmin):
        tree.heading('Edit', text='Edit')
        tree.column('Edit', width=100, anchor='center')
    tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    for project in projectsView :
        tree.insert('', tk.END, values=(project["title"], statuses[project["status"]+1], "Edit"), tag = (project["id"]))

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
