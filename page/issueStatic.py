import tkinter as tk
from tkinter import ttk

import page.api as api
import page.issueList as issuelist
import page.login as login
import page.issueDetail as issue

session = ""
projectId = 0
static = {}
page_move = {}

static_category = ["new-issue", "closed-issue", "best-member", "best-issue"]
period = ["daily", "monthly"]
users = ["pl", "dev", "tester"]

sections = ["Daily Issue Count", "Monthly Issue Count", "Daily Closed Issue", "Monthly Closed Issue", "Best PL", "Best Dev", "Best Tester", "Daily Top3 Issue", "Monthly Top3 Issue"]
buttons = [
        ("Issue Count", ["Daily Issue Count", "Monthly Issue Count"]),
        ("Closed Issue", ["Daily Closed Issue", "Monthly Closed Issue"]),
        ("Best", ["Best PL", "Best Dev", "Best Tester"]),
        ("Top3 Issue", ["Daily Top3 Issue", "Monthly Top3 Issue"])
    ]

# 로그아웃    
def logout(view):
    print("logout")
    api.logout(session)
    login.loginView(view, session)

def back(view):
    print("back")
    issuelist.issuelist(view, projectId, session)

# Function to show the appropriate frame
def show_frame(frame):
    frame.tkraise()

def on_listbox_select(view, event, listbox):
    selected = listbox.curselection()
    if selected:
        item_text = listbox.get(selected)
        issue.issueDetail(view, projectId, page_move[item_text], session)
    
def get_static() :
    global static
    print(static)
    static = api.get_static(projectId, session)

def issueStaticView(view, projectID, projectTitle, session_get) :
    global session
    global projectId
    global page_move

    projectId = projectID
    session = session_get
    page_move = {}
    get_static()

    for widget in view.winfo_children():
        widget.destroy()

    view.geometry("500x450")
    view.title("Issue Tracker")

    # Title frame at the top
    title_frame = tk.Frame(view)
    title_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    # Title
    title_label = tk.Label(title_frame, text="Issue", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, padx=2, pady=10, sticky="w")

    # ProjectName
    project_name_label = tk.Label(title_frame, text=f"/{projectTitle}", font=("Helvetica", 16))
    project_name_label.grid(row=0, column=1, padx=2, pady=10, sticky="w")

    # Button frame at the top right
    button_frame = tk.Frame(title_frame)
    button_frame.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    # Back button
    back_button = tk.Button(button_frame, text="back", command=lambda: back(view))
    back_button.grid(row=0, column=0, padx=5, sticky="e")

    # Logout button
    logout_button = tk.Button(button_frame, text="logout", command=lambda: logout(view))
    logout_button.grid(row=0, column=1, padx=5, sticky="e")

    # Create frames for the left sidebar and the main content area
    sidebar = ttk.Frame(view, width=200, relief="sunken")
    sidebar.grid(row=1, column=0, sticky="ns")

    container = ttk.Frame(view)
    container.grid(row=1, column=1, sticky="nsew")

    # Configure rows and columns to expand properly
    view.grid_rowconfigure(1, weight=1)
    view.grid_columnconfigure(1, weight=1)

    # Create a frame for each section
    frames = {}
    for cat in static_category:
        frames[cat] = {}
        if(cat == "new-issue" or cat == "closed-issue") :
            for day in period : 
                frame = ttk.Frame(container)
                frame.grid(row=0, column=0, sticky="nsew")
                
                static_label = tk.Label(frame, text=f"{cat}_{day}", font=("Helvetica", 16))
                static_label.grid(row=0, column=0, padx=2, pady=10, sticky="w")

                frames[cat][day] = frame
                listbox = tk.Listbox(frame, font=("Arial", 10), width=45, height=15)
                
                for static_data in static[cat][day]["data"] :
                    listbox.insert(tk.END, f"날짜 : {static_data['date']} , {cat}개수 {static_data['count']}")
                listbox.grid(row=1, column=0, sticky='nsew')
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)
        elif(cat == "best-member") :
            for user in users :
                frame = ttk.Frame(container)
                frame.grid(row=0, column=0, sticky="nsew")

                static_label = tk.Label(frame, text=f"{cat}_{user}", font=("Helvetica", 16))
                static_label.grid(row=0, column=0, padx=2, pady=10, sticky="w")

                frames[cat][user] = frame
                listbox = tk.Listbox(frame, font=("Arial", 10), width=45, height=15)
                static_data = static[cat]["weekly"]["data"][user] 
                listbox.insert(tk.END, f"사용자 {static_data['username']}, {user}로 등록된 issue 개수 {static_data['count']}개")
                listbox.grid(row=1, column=0, sticky='nsew')
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)
        else :
            for day in period : 
                frame = ttk.Frame(container)
                frame.grid(row=0, column=0, sticky="nsew")

                static_label = tk.Label(frame, text=f"{cat}_{day}", font=("Helvetica", 16))
                static_label.grid(row=0, column=0, padx=2, pady=10, sticky="w")

                frames[cat][day] = frame
                listbox = tk.Listbox(frame, font=("Arial", 10), width=45, height=15)
                for static_data in static[cat][day]["data"] :
                    temp = f"제목 : {static_data['title']} , comment 개수 {static_data['count']}"
                    listbox.insert(tk.END, temp)
                    page_move[temp] = static_data["issueId"]
                listbox.bind("<<ListboxSelect>>", lambda event : on_listbox_select(view, event, listbox))
                listbox.grid(row=1, column=0, sticky='nsew')
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)
    
    for idx, (category, items) in enumerate(buttons):
        category_label = ttk.Label(sidebar, text=category, font=("Arial", 10, "bold"))
        category_label.grid(row=idx*5, column=0, sticky="w", padx=10, pady=5)
        for jdx, item in enumerate(items):
            if(idx!=2) :
                button = ttk.Button(sidebar, text=item, command=lambda idx=idx, jdx=jdx: show_frame(frames[static_category[idx]][period[jdx]]))
            else :
                button = ttk.Button(sidebar, text=item, command=lambda idx=idx, jdx=jdx: show_frame(frames[static_category[idx]][users[jdx]]))
            button.grid(row=idx*5 + jdx + 1, column=0, sticky="w", padx=20)
    