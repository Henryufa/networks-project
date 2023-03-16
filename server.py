#Server source code
#Henry Bahr, hwbfd6, 16259142
#3-14-23
#Run this program then run client.py. After doing so client will be able to login, send messages, create a new user, and logout

import socket
import os.path
 
USERS_FILE = "users.txt"

def logged_in(userid):
    if userid == "":
        return False
    else:
        return True

#allows for max message length of 9,999,999,999 characters
HEADER_DIGITS = 10
#define acceptable commands
LOGIN = "login"
NEWUSER = "newuser"
SEND = "send"
LOGOUT = "logout"
SUCCESS = "success"
FAILURE = "failure"
#add minimum users to users file
def load_users():
    if os.path.isfile(USERS_FILE) is False:
        users = {
            "Tom" : "Tom11",
            "David" : "David22",
            "Beth" : "Beth33"
        }

        with open(USERS_FILE,"w") as f:
            for key, value in users.items():
                f.write(f"({key}, {value})\n")
    users = []
    with open(USERS_FILE,"r") as f:
        for line in f:
            users.append(line.strip()[1:-1].split(","))
    for user in users:
        user[1] = user[1].strip()
    print(users)
    f.close()
    return users

def send_with_header(clientsocket,msg):
    msg = f"{len(msg):<{HEADER_DIGITS}}" + msg
    clientsocket.send(bytes(msg,"utf-8"))

def login_func(clientsocket,msg,current_userid):
    if logged_in(current_userid) == False:
        send_with_header(clientsocket,"Denied. Please logout first.")
    if msg[0].lower() == LOGIN and len(msg) == 3:
        user_info = [msg[1],msg[2]]
        if user_info in load_users():
            current_userid = msg[1]
            print(f"login of {user_info} was successful")
            send_with_header(clientsocket,"login successful")
            return current_userid
        else:
            send_with_header(clientsocket,"login failed")
            print(f"Someone tried to login with {user_info} but that user is not in our records")
            return current_userid

def new_user_func(clientsocket,msg,current_userid):
    if logged_in(current_userid) == False:
        send_with_header(clientsocket,"Denied. Please logout first.")
    if msg[0].lower() == NEWUSER and len(msg) == 3:
        user_id = msg[1]
        for user in load_users():
            if user_id == user[0]:
                send_with_header(clientsocket,"Denied. User account already exists.")
                print(f"that user {msg[1]} is already in our system")
                return current_userid
        with open(USERS_FILE,"a") as f:
            f.write(f"({msg[1]}, {msg[2]})\n")
        print("new user added to db")
        f.close()
        send_with_header(clientsocket,"New user account created. Please login.")
        return current_userid
    else:
        send_with_header(clientsocket,"could not create new user")
        print("You attempted to issue a new user command, but it was not formatted correctly\nThe format is: \"newuser UserID Password\"  \nUserID is between 3 and 32 characters and Password is between 4 and 8 characters in length")
        return current_userid

def send_func(clientsocket,msg,current_userid):
    if logged_in(current_userid) == False:
        send_with_header(clientsocket,"Denied. Please login first.")
    if msg[0].lower() == SEND and len(msg) == 2:
        send_with_header(clientsocket,current_userid + " " + msg[1])
        return current_userid
    else:
        send_with_header(clientsocket,"could not send message")
        print("You attempted to issue a send message command, but it was not formatted correctly\nThe format is: \"send message\"  \nmessage is between 1 and 256 characters")
        return current_userid  

def logout_func(clientsocket,msg,current_userid):
    if logged_in(current_userid) == False:
        send_with_header(clientsocket,"Denied. You are not logged in.")
    if msg[0].lower() == LOGOUT and len(msg) == 1:
        current_userid = ""
        print("clientsocket has been closed")
        send_with_header(clientsocket,SUCCESS)
        clientsocket.close()
        return True
    send_with_header(clientsocket,FAILURE)
    return False

#create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#declare the IP address and port
IP = "127.0.0.1"

PORT = 19142

#Bind the socket to the specified IP address and port
s.bind((IP,PORT))

s.listen()

#listen forever
while True:
    
    #accept all connections and store their socket object, and IP address
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established")
    current_userid = ""
    while True:
        # try:
        print("I am here")
        msg_length = clientsocket.recv(HEADER_DIGITS)
        print(msg_length)
        msg_raw = clientsocket.recv(int(msg_length.decode("utf-8"))).decode("utf-8")
        print("received message: " + msg_raw)
        # except:
        #     break
        msg = msg_raw.split()
        print("the parsed message is: ", msg)
        if msg[0].lower() == LOGIN and len(msg) == 3:# and logged_in(current_userid) == False:
            current_userid = login_func(clientsocket, msg, current_userid)

        elif msg[0].lower() == NEWUSER and len(msg) == 3:# and logged_in(current_userid) == False:
            current_userid = new_user_func(clientsocket, msg, current_userid)

        elif msg[0].lower() == SEND and len(msg) >= 2:# and logged_in(current_userid) == True:
            msg = [msg[0], ' '.join(msg[1:])]
            current_userid = send_func(clientsocket,msg, current_userid)

        elif msg[0].lower() == LOGOUT and len(msg) == 1:
            print("entered logout func")
            if logout_func(clientsocket,msg, current_userid) == True:
                print("logout successful")
                break
        else:
            send_with_header(clientsocket,"your command could not be processed")
            print(f"You entered \"{msg_raw}\", this is not a valid command or you must login/logout to perform it. Please enter one of the following commands\nlogin UserID Password\nnewuser UserID Password\nsend message\nlogout")

        print(f"current_userid = {current_userid}")
