#Client source code
#Henry Bahr, hwbfd6, 16259142
#3-14-23
#Run server.py then run this program. After doing so client will be able to login, send messages, create a new user, and logout

import socket

#messages can be up to 9,999,999,999 characters in length
HEADER_DIGITS = 10
LOGIN = "login"
NEWUSER = "newuser"
SEND = "send"
LOGOUT = "logout"
SUCCESS = "success"
FAILURE = "failure"

def login_func(msg):
    if msg[0].lower() == LOGIN and len(msg) == 3 and 3 <= len(msg[1]) and len(msg[1]) <= 32 and 4 <= len(msg[2]) and len(msg[2]) <= 8:
        msg = msg[0] + " " + msg[1] + " " + msg[2]
        msg = f"{len(msg):<{HEADER_DIGITS}}" + msg
        s.send(bytes(msg,"utf-8"))
        return True
    else:
        print("You attempted to issue a login command, but it was not formatted correctly\nThe format is: \"login UserID Password\"\nUserID is between 3 and 32 characters and Password is between 4 and 8 characters in length")
        return False

def new_user_func(msg):
    if msg[0].lower() == NEWUSER and len(msg) == 3 and 3 <= len(msg[1]) and len(msg[1]) <= 32 and 4 <= len(msg[2]) and len(msg[2]) <= 8:
        msg = msg[0] + " " + msg[1] + " " + msg[2]
        msg = f"{len(msg):<{HEADER_DIGITS}}" + msg
        s.send(bytes(msg,"utf-8"))
        return True
    else:
        print("You attempted to issue a new user command, but it was not formatted correctly\nThe format is: \"newuser UserID Password\"  \nUserID is between 3 and 32 characters and Password is between 4 and 8 characters in length")
        return False

def send_func(msg):
    if msg[0].lower() == SEND and len(msg) == 2 and 1 <= len(msg[1]) and len(msg[1]) <= 256:
        msg = msg[0] + " " + msg[1]
        msg = f"{len(msg):<{HEADER_DIGITS}}" + msg
        s.send(bytes(msg,"utf-8"))
        return True
    else:
        print("You attempted to issue a send message command, but it was not formatted correctly\nThe format is: \"send message\"  \nmessage is between 1 and 256 characters")
        return False  

def logout_func(msg):
    if msg[0].lower() == LOGOUT and len(msg) == 1:
        msg = msg[0]
        msg = f"{len(msg):<{HEADER_DIGITS}}" + msg
        s.send(bytes(msg,"utf-8"))
        print("sent logout message to server")
        msg_length = s.recv(HEADER_DIGITS)
        msg_raw = s.recv(int(msg_length.decode("utf-8"))).decode("utf-8")
        print("received message: " + msg_raw)
        return msg_raw == SUCCESS
    return False

#create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "127.0.0.1"
PORT = 19142
s.connect((IP,PORT))


while True:
    #issue command
    msg_raw = input("Enter a command: ")
    msg = msg_raw.split()
    print("the command you entered is: ", msg)

    if msg[0].lower() == LOGIN and len(msg) == 3:
        if login_func(msg) == False:
            continue

    elif msg[0].lower() == NEWUSER and len(msg) == 3:
        if new_user_func(msg) == False:
            continue

    #change this so that message
    elif msg[0].lower() == SEND and len(msg) >= 2:# and 1 <= len(' '.join(msg[1:])) and len(' '.join(msg[1:])) <= 256 :
        msg = [msg[0], ' '.join(msg[1:])]
        if send_func(msg) == False:
            continue

    elif msg[0].lower() == LOGOUT and len(msg) == 1:
        print("entered logout block")
        if logout_func(msg) == True:
            break
        else:
            continue

    else:
        print(f"You entered \"{msg_raw}\", this is not a valid command. Please enter one of the following commands\nlogin UserID Password\nnewuser UserID Password\nsend message\nlogout")
        continue
    #receive message
    msg_length = s.recv(HEADER_DIGITS)
    msg_raw = s.recv(int(msg_length.decode("utf-8"))).decode("utf-8")
    print("received message: " + msg_raw)


# msg_length = len(msg)
# msg = f"{msg_length:<{HEADER_DIGITS}}" + msg
# s.send(bytes(msg,"utf-8"))

#accept a message with 16 bytes or less
'''
BUFFER_SIZE = 16
full_msg = ''
new_msg = True
msg_length = 0
while True:
    msg = s.recv(BUFFER_SIZE)
    full_msg += msg.decode("utf-8")
    if new_msg:
        msg_length = int(msg[:HEADER_DIGITS])
        print(f"message length is {msg_length}")
        new_msg = False
    if len(full_msg) == msg_length + HEADER_DIGITS:
        print(f"{full_msg[HEADER_DIGITS:]}")
        new_msg = True
        full_msg = ''
        msg_length = 0



print(msg.decode("utf-8"))
'''
