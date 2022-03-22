import requests 


#token = ""
Session = requests.Session()  #Create a session 
#cookies = {}
def register(username,email,password):
    user_data = {'username': username, 'email':email,'password':password}
    request = requests.post("http://127.0.0.1:8000/register",data=user_data)
    print(request.text)

def login(username,password):
    Session = requests.Session()  #Create a session 

    user_data = {'username': username, 'password':password}

    Session = requests.post("http://127.0.0.1:8000/login",data=user_data)
    cookies = dict(Session.cookies)
    print(Session.text)
       
    token = Session.cookies['csrftoken']
    #print(token)
    return cookies,token

def logout():
    request = Session.get("http://127.0.0.1:8000/logout_user", cookies=cookies)
    print(request.text)

def list():
    request = requests.get("http://127.0.0.1:8000/list")
    response_text_temp = request.text
    response_text_temp = response_text_temp[1:]
    response_text_temp = response_text_temp[:-1]

    response_text = response_text_temp.split(",")

    for text in response_text:
        print(text[1:-1])

def view():
    request = Session.get("http://127.0.0.1:8000/view")
    

    response_text_temp = request.text
    response_text_temp = response_text_temp[1:]
    response_text_temp = response_text_temp[:-1]

    response_text = response_text_temp.split(",")

    for text in response_text:
        print(text)

def average(prof_id, mod_code):
    user_data = {'csrfmiddlewaretoken': token,'prof':prof_id,'mod':mod_code, }
    request = Session.post("http://127.0.0.1:8000/average",data=user_data,cookies=cookies)
    text = request.text
    text = text[3:-3]
    print(text)

def rate(prof_id,mod_code,year,sem,rating):
    #token = Session.cookies['csrftoken']
    #print(token)
    user_data = {'csrfmiddlewaretoken': token,'prof':prof_id,'mod':mod_code,'year':year,'sem':sem,'rating':rating}
    request = Session.post("http://127.0.0.1:8000/rate",data=user_data,cookies=cookies)
    print(request.text)


while(1):
    
    user_input = input("Please enter a command ('q' to quit): ")

    if user_input == "register":
        username = input("Please enter a username: ")
        email = input("Please enter an email address: ")
        password = input("Please enter a password: ")
        register(username,email,password)

    elif user_input == "login": #TODO ADD URL
        username = input("Please enter a username: ")
        password = input("Please enter a password: ")
        return_vals = login(username,password)
        cookies = return_vals[0]
        token = return_vals[1]
        #token = Session.cookies['csrftoken']
    elif user_input == "logout": 
        
        logout()
        
    elif user_input == "list":
        list()

    elif user_input == "view":
        view()
        
    elif "average" in user_input:
        user_input_split = user_input.split()
        average(user_input_split[1],user_input_split[2])
    elif "rate" in user_input:
        user_input_split = user_input.split()
        rate(user_input_split[1],user_input_split[2],user_input_split[3],user_input_split[4],user_input_split[5])
    elif user_input == "q":
        quit()
    else:
        print("Command not recognized! ")
    
    #rate JE1 CD1 2017 1 2
        
        

