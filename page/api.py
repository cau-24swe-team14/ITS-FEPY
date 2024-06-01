import requests as req

url = "http://127.0.0.1:8080/"

# 회원 가입
def signup(id, password, session):
    try:
        # 서버와 연결하여 회원가입 처리
        signup_data = {'username': id, 'password': password}
        res = session.post(url + "users/signup", json=signup_data)
        
        if res.status_code == 201:
            return True
        else:
            return False
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False

# 서버와 연결해서 로그인 할 수 있도록
def loginCheck(id, password, session):
    try:
        login_data = {'username': id, 'password': password}
        res = session.post(url + "users/login", json=login_data)
        print(res.status_code)
        if res.status_code == 200:
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
            print(data)
            return True, res
        else:
            return False, {}
    except req.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False