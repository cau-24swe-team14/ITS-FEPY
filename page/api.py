import requests as req

url = "http://127.0.0.1:8080/"
username = ""

# 회원 가입
def signup(id, password, session):
    global username
    try:
        # 서버와 연결하여 회원가입 처리
        signup_data = {'username': id, 'password': password}
        res = session.post(url + "users/signup", json=signup_data)
        
        if res.status_code == 201:
            username = id
            return True
        else:
            return False
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False

# 서버와 연결해서 로그인 할 수 있도록
def loginCheck(id, password, session):
    global username
    try:
        login_data = {'username': id, 'password': password}
        res = session.post(url + "users/login", json=login_data)
        if res.status_code == 200:
            username = id
            return True
        else:
            return False
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
# 프로젝트 리스트 가져오기
def getProjectData(session):
    try:
        res = session.get(url + "projects")
        if res.status_code == 200:
            data = res.json()
            if(data["isAdmin"] == 1) :
                return True, data["project"]
            else : 
                return False, data["project"]
        else:
            return False, {}
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False

# 유저 존재 여부 확인
def check_user(username, session) :
    try:
        res = session.get(url + f"users/isExist?username={username}")
        if res.status_code == 200 :
            return True
        else:
            return False
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
# 프로젝트 생성
def create_project(create, session) :
    try:
        res = session.post(url + "projects", json=create)
        if res.status_code == 201:
            print("create project!")
            return True
        else:
            return False
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
# 프로젝트 데이터 가져오기
def project_data(project_id, session) :
    try:
        res = session.get(url + f"projects/{project_id}")
        if res.status_code == 200:
            data = res.json()
            return True, data
        else:
            return False, {}
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
# 프로젝트 수정
def edit_project(edit, project_id, session) :
    try :
        res = session.patch(url + f"projects/{project_id}", json = edit)
        if(res.status_code == 204) :
            return True
        else :
            return False
    except req.exceptions.RequestException as e:
        print(f'An error occurred while updating project: {e}')
        return False
    
# 로그 아웃
def logout(session) :
    try:
        session.get(url + f"users/logout")
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
# 이슈 리스트 가져오기
def getIssueData(session, project_id):
    try:
        res = session.get(url + f"projects/{project_id}")
        if res.status_code == 200:
            data = res.json()
            if(data["accountRole"] == 2) : # 사용자가 테스터
                return True, data
            else : 
                return False, data
        else:
            return False, {}
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False

# 이슈 내용 가져오기
def getIssue(projectId, issueId, session) :
    try:
        res = session.get(url + f"projects/{projectId}/issues/{issueId}")
        if res.status_code == 200:
            data = res.json()
            return data
        else:
            return False, {}
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False

# 이슈 검색
def search(projectId, context, search_filter, session) :
    try:
        print(url + f"projects/{projectId}/issues?{search_filter}={context}")
        res = session.get(url + f"projects/{projectId}/issues?{search_filter}={context}")
        if res.status_code == 200:
            data = res.json()
            return data
        else:
            return False, {}
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
# 이슈 생성
def create_issue(projectId, create, session) : 
    try:
        res = session.post(url + f"projects/{projectId}/issues", json=create)
        if res.status_code == 201:
            print("create issues!")
            return True
        else:
            return False
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
# 이슈 수정
def edit_issue(projectId, issueId, edit, session) :
    try :
        res = session.patch(url + f"projects/{projectId}/issues/{issueId}", json = edit)
        if(res.status_code == 204) :
            return True
        else :
            return False
    except req.exceptions.RequestException as e:
        print(f'An error occurred while updating project: {e}')
        return False

# dev 추천 
def recommend(projectId, issueId, session) :
    try:
        res = session.get(url + f"projects/{projectId}/issues/{issueId}/assignee-suggestions")
        if res.status_code == 200:
            return res.json()["username"]
        else:
            return "No recommended Dev"
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
# 댓글 작성
def comment_issue(projectId, issueId, comment, session) : 
    try:
        res = session.post(url + f"projects/{projectId}/issues/{issueId}/comments", json=comment)
        if res.status_code == 201:
            return True
        else:
            return False
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
# 통계 정보 가져오기
def get_static(projectId, session) :
    category = ["new-issue", "closed-issue", "best-issue", "best-member"]
    try:
        static = {}
        for cat in category :
            res = session.get(url + f"projects/{projectId}/trend?category={cat}")
            if res.status_code != 200: print(res.status_code)
            static[cat] = res.json()
        return static
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False