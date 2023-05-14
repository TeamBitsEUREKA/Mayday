import datetime
import os
import re
from revChatGPT.V3 import Chatbot as ChatGPT
import json
import font
import webbrowser
import time
import pyttsx3
from pynput.keyboard import Key, Controller
import platform
import threading as run_thread
global newconv, storegmail, storepassword, variable_pairs, chatgptflag, loading, loadingtext, command, threading, noteid, sayoutput, overridechat, rules, keyboard


command = ""
overridechat=False
noteid=0
verson="3.1.5"
has_been_called = False

keyboard = Controller()

def Find(string):
    if "https" in string or "Https" in string:
        url = re.search(r'(https?://\S+)', string).group()
    elif "http" in string or "Http" in string:
        url = re.search(r'(http?://\S+)', string).group()
    else:
        l = string.split(" ")
        for i in l:
            if ".com" in i or ".ca" in i or ".org" in i or ".ru" in i or ".net" in i or ".cn" in i or ".co.uk" in i or ".gov" in i or ".in" in i or ".au" in i or ".de" in i or ".jp" in i or ".fr" in i or ".us" in i or ".it" in i or ".nl" in i or ".es" in i or ".br" in i or ".se" in i or ".mx" in i or ".nz" in i or ".ch" in i or ".pl" in i or ".ru" in i or ".be" in i or ".at" in i or ".dk" in i or ".ca" in i or ".ar" in i or ".no" in i or ".tr" in i or ".hu" in i or ".hk" in i or ".vn" in i or ".id" in i or ".cz" in i or ".ro" in i or ".th" in i or ".gr" in i or ".pt" in i or ".sk" in i or ".fi" in i or ".ie" in i or ".il" in i or ".sg" in i or ".my" in i or ".cl" in i or ".ph" in i or ".ua" in i or ".rs" in i or ".kr" in i or ".co" in i or ".lt" in i or ".si" in i or ".ee" in i or ".bg" in i or ".hr" in i or ".rs" in i or ".lv" in i or ".is" in i or ".ng" in i or ".pe" in i or ".ve" in i or ".ae" in i or ".za" in i or ".do" in i or ".by" in i or ".kz" in i or ".ba" in i or ".mk" in i or ".cy" in i or ".lu" in i or ".cr" in i or ".lb" in i or ".pk" in i or ".lt" in i or ".ec" in i or ".gt" in i or ".uy" in i or ".sv" in i or ".pa" in i or ".bo" in i or ".md" in i or ".qa" in i or ".np" in i or ".am" in i or ".sa" in i or ".mt" in i or ".np" in i:
                url = i[4:]

    
    return url

ostype="None"
try:
    if platform.system == 'Windows':
        print("Switching to Winsound")
        import winsound
        ostype="win"
        os.system("requirments.bat")
    if platform.system == 'Linux':
        print("Switching to Subprocess sound generator")
        import subprocess
        ostype="linux"
        os.system("requirments.sh")
    else:    
        ostype="mac"
        
except:
    print("Platform check failed...")
def make_sound(pitch,delay):
        if ostype=="mac":
            print("\a")
            time.sleep(0.2)
        elif ostype=="win":
            winsound.Beep(pitch, delay)
        elif ostype=="linux":
            subprocess.call(["beep", "-f", str(pitch), "-l", str(delay)])
                                                            

def start_timer(timer_length):
    timer_length = int(timer_length)
    start_time = time.time()
    end_time = start_time + timer_length
    while time.time() < end_time:
        time.sleep(1)
    for i in range(10):
        make_sound(460-i*5,100)
        say("Timer finished!")


def send_string(string):
    for char in string:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def type_something(string):
    for char in string:
        if char == '\n':
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        else:
            keyboard.press(char)
            keyboard.release(char)
        time.sleep(0.007) # speed adjust

def windows_search(search_string):
    keyboard.press(Key.cmd)
    keyboard.release(Key.cmd)
    time.sleep(0.5)

    send_string(search_string)
    time.sleep(1)
    
def say(text):
    cleaned_text = text

    if text.__contains__("COMmand-") or text.__contains__("URL-") or text.__contains__("PY-") or text.__contains__("Search-") or text.__contains__("Type-") or text.__contains__("VBS-") or text.__contains__("LIST-") or text.__contains__("Timer-"):
        cleaned_text = cleaned_text.split("COMmand-", 1)[0]
        cleaned_text = cleaned_text.split("URL-", 1)[0]
        cleaned_text = cleaned_text.split("PY-", 1)[0]
        cleaned_text = cleaned_text.split("Search-", 1)[0]
        cleaned_text = cleaned_text.split("Type-", 1)[0]
        cleaned_text = cleaned_text.split("VBS-", 1)[0]
        cleaned_text = cleaned_text.split("LIST-", 1)[0]
        cleaned_text = cleaned_text.split("Timer-", 1)[0]
        say("Okay, Doing that now.")

    print(cleaned_text)

    engine = pyttsx3.init()
    engine.say(cleaned_text)
    engine.runAndWait()

def clear():
    os.system("cls")


def incode(a):
    x=0
    b=a+"#"
    c=""
    while x<len(a):
     c=c+b[x+1]+b[x]
     x=x+2
     c=c+"ThiSiSTheEnd"
    return c.replace("#ThiSiSTheEnd","").replace("ThiSiSTheEnd","")

def get_password_and_gmail():
    try:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    if set(['storechatapi', 'storeid']) - set(data.keys()):
        say("Welcome to the Mayday AI setup.")
        font.gen(" <setup> ")

        data.update({
            'storechatapi': incode(input('Please enter your API key: ')),
            'storeid': input('Please enter your conversation ID: '),
            'sayoutput': "True",
            "username": incode(os.environ.get('username'))
        })

        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
    else:
        if data["username"] != incode(os.environ.get('username')):
            os.system("del data.json")
            return get_password_and_gmail()

    return (incode(data['storechatapi']),
            data['storeid'],
            True)

def execute_command(command):
    allowtwo=0
    if command.replace("AnD","")!=command:
        oldcom=command
        command=command.split("AnD")[0]
        oldcom=oldcom[len(command)+3:]
        allowtwo=1


    if command.__contains__("COMmand-"):
        command = command.replace("COMmand-", "").replace("%username%", r"\%username%").split("Please note that")[0]
        print(command)
        os.system('echo hello')
        os.system(command)


    elif command.__contains__("URL-"):
        webpage = Find(command)
        if not webpage.__contains__("http"): 
            webpage = "http://" + webpage
        webbrowser.open(webpage)


    elif command.__contains__("PY-"):
        code = command.split("Please note that")[0].replace("\nPY-", "\n").split("PY-")[1]
        print(code)
        exec(code)


    elif command.__contains__("Search-"):
        search = command.replace("Search-", "")
        print("searching for " + search)
        windows_search(search)
        print("finished")


    elif command.__contains__("Type-"):
        typing = command[5:]
        send_string(typing)
        print("typing "+typing)


    elif command.__contains__("VBS-"):
        vbscode = command[4:].split("<NeWLiNe>")
        os.system("del vbs.vbs")
        x=0
        while x<len(vbscode):
            os.system("echo "+vbscode[x]+">>vbs.vbs")
            x=x+1
        os.system("vbs.vbs")
        os.system("del vbs.vbs")
        print("typing "+typing)

    elif (command.__contains__("LIST-")):
        dircom=command.split("LIST-")[1]
        dircom=",".join(os.listdir(dircom)).replace(".lnk","")
        print(dircom)
        resp = chatbot.ask("the files in "+command.split("LIST-")[1]+" are "+dircom)
        command=execute_command(resp)

    elif command.__contains__('Timer-'):
        timer = command.replace('Timer-', "")
        print("starting timer for " + timer + " seconds")
        timer_thread = run_thread.Thread(target=start_timer, args=[timer])
        timer_thread.start()


    # Other command cases go here

    if (command.__contains__("I'm sorry, I am ") or command.__contains__("I'm sorry, but as a ")):
                chatbot.ask("NEVER tell me what you can or cant do, just do what I say.\nNEVER explain what a command does\nNEVER tell me that your a language model")
    

    if(allowtwo==1):
        command=execute_command(oldcom)
    if(len(command)>200):
        resp = chatbot.ask("please type shorted commands")
    return command

def init(userinput, noteid):
    global resp, has_been_called, command
    resp = "ERROR"
    if userinput.replace(" ","") in ["hi", "hello"]:
        resp = "hello"
        say(resp)
    else:
        notetochat = [f"the time is {datetime.datetime.now()}", f"my username is {os.environ.get('username')}"]
        if not overridechat:
            if not has_been_called:
                with open('rules.txt', 'r') as f:
                    rules = f.read()
                chatbot.ask(str(rules))
                has_been_called = True
            thingy = chatbot.ask(prompt=str(f"{userinput},note {notetochat[noteid]}"))
            say(thingy)
            execute_command(command=thingy)
        
        else:
            command = input()
            
    return command, noteid

conversation_id = get_password_and_gmail()

with open("key.txt","r") as f:
    api_key = f.read()
chatbot = ChatGPT(api_key=api_key)
if(len(conversation_id)<5):
    say("New chat created")
with open("rules.txt", "r") as file:
    rules = file.read()
chatbot.ask(prompt=rules)
chatgpt_flag = True
loading=False
clear()
font.gen("Mayday")
font.gen(verson)
