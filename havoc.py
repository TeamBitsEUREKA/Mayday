import datetime
import os
import re
from revChatGPT.V3 import Chatbot as ChatGPT
import json
import font
import webbrowser #cmd:we should probly allow this to be used if someone doesnt want to give out there api key - KevinE: umm, idk maybe, wont bother with it
import time#cmd:why\|/ - KevinE: IDK keep it in case the OS feels like its loosing track of the time
#cmd:and all related code is missing
import pyttsx3
from pynput.keyboard import Key, Controller # required to search local computer through windows search
import time#cmd:then del this one<--- - KevinE: if the OS sleeps through the first time we can remind it with the second!!
import platform
import threading as run_thread
#someone:imports/|\
global newconv, storegmail, storepassword, variable_pairs, chatgptflag, loading, loadingtext, command, threading, noteid, sayoutput, overridechat, rules, keyboard
command = ""

#set globals
overridechat=False # KevinE: You shouldnt need to touch any of these, but as a breif overview. overridechat allows you to override voice commands, usefull if you are testing a new feature
#app_password="" # just ignore this, idk what it is, I forgot what I was planning to do with it. KevinE: oh, well somebody put it in a comment...
#cmd:my guess is that its for the old google login
#cmd: it can likly be removed
#cmd:has been removed
api_key_chatgpt=""

noteid=0#cmd:why do we still have gnote code
verson="3.1.5" # KevinE: Version number, printed at the start if the program
has_been_called = False # Sendrules 
# KevinE: Define a function to send a string of characters to the active window

keyboard = Controller()
#cmd:detect os

def Find(string):
 
    # findall() has been used
    # with valid conditions for urls in string
    if "https" in string or "Https" in string:
        url = re.search(r'(https?://\S+)', string).group()
    return url

ostype="what"
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
        #print("Unable to identify OS type, defaulting to legacy")
        
except:
    print("how?")
    print("platform check failed...") # KevinE: print("Good luck")
def make_sound(pitch,delay): # We needed this in order to change the sound API depending on the OS
        #CMD:moved os detection to the top of the file
        if ostype=="mac":
            print("\a")
            time.sleep(0.2)
        elif ostype=="win":
            winsound.Beep(pitch, delay)
        elif ostype=="linux":
            subprocess.call(["beep", "-f", str(pitch), "-l", str(delay)])
        #from AppKit import NSSsound # KevinE: F*ck you apple, you managed to make the only os in the ENTIRE WORLD which dosent recognize subprocess...
        #duration = 1#cmd:censered/|\                        #
        #frequency = 440                                     #
        #sound = NSSsound.alloc().initWithData_(None)        #
        #sound.setDelegate_(None)                            #
        #sound.initWithFrequency_(frequency)                 #
        #sound.setVolume(1)                                  # add shit here (KevinE)
        #start_time = time.time()                            #
        #while time.time() - start_time < duration:          #
        #    sound.play                                      #
                                                            ##
                                                            ##
                                                            ##
        #cmd: someone delete this /|\
        #cmd: as i already rewrote it
                                                            

def start_timer(timer_length):
    timer_length = int(timer_length)  #kevinE:convert the timer length to an integer,cmd:why a int?
    start_time = time.time()
    end_time = start_time + timer_length
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        print(f"Timer: {remaining_time} seconds left.")#cmd:do we realy need this in termal
        time.sleep(1)
    print("Timer finished!")
    for i in range(10):
        make_sound(460-i*5,100)


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

# Define a function to search for a string in the Windows search bar
def windows_search(search_string):
    # Simulate Windows key press to open search bar
    keyboard.press(Key.cmd)
    keyboard.release(Key.cmd)
    time.sleep(0.5)

    # Send the search string to the search bar and press Enter to initiate search
    send_string(search_string)
    time.sleep(1)

def say(text): # call the TTS engine for your OS
    #the current tts engine
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

def clear(): # Clears the screen
    os.system("")

def loading_animation(loading_text): # Loading animation, is not used after switching from webscraping (PyChatGPT, we had to wait to load the website) to on demmand results using revChatGPT API
    while loading:
        for frame in [" .", "  >", " ' ", " <"]:
            clear()
            font.gen(loading_text + frame) # You can use Font.get to generate font using our font engine 
            time.sleep(0.25) # Time between frames
    clear()

def incode(a):
    x=0
    b=a+"#"
    c=""
    while x<len(a):
     c=c+b[x+1]+b[x]
     x=x+2
     c=c+"ThiSiSTheEnd"
    return c.replace("#ThiSiSTheEnd","").replace("ThiSiSTheEnd","")

def get_password_and_gmail(): # Bunch of code that returns the details used for the ChatGPT API. WE NEED TO FIX THIS IT IS NOT WORKING
    try:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    if set(['storechatapi', 'storeid']) - set(data.keys()):
        say("Welcome to the HAL engine")
        font.gen(" <setup> ")

        data.update({
            'storechatapi': incode(input('Please enter your API key: ')),
            'storeid': input('Please enter your conversation ID: '),
            'sayoutput': "True",
            "username": incode(os.environ.get('username'))
        })
        #cmd:this doesnt look for the api key only the google password 

        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
    else:
        if data["username"] != incode(os.environ.get('username')):
            os.system("del data.json")
            return get_password_and_gmail()

    return (incode(data['storechatapi']),
            data['storeid'],
            True)

api_key_chatgpt, conversation_id, sayoutput = get_password_and_gmail()

string_acess_token = str(api_key_chatgpt) #this is because if I directly write acess token it dosent work, for some reason.
chatbot = ChatGPT(api_key='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')
#for everyones sake put this(/|\) in the json file
#cmd:done
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
CMD = "0000"
DOOR1 = "0005"
LIGHT1 = "0001"
LIGHT2 = "0002"
LIGHT3 = "0003"
LIGHT4 = "0004"



def execute_command(command):

    allowtwo=0
    if command.replace("AnD","")!=command:
        oldcom=command
        command=command.split("AnD")[0]
        oldcom=oldcom[len(command)+3:]
        allowtwo=1


    if command.__contains__("COMmand-"): # Run local CMD commands
        command = command.replace("COMmand-", "").replace("%username%", r"\%username%").split("Please note that")[0]
        print(command)
        os.system('echo hello')
        os.system(command)


    elif command.__contains__("URL-"): # Open web pages
        # webpage = command.split("Please note that")[0].split("RL-")[1].split("\n")[0]
        webpage = Find(command)
        if not webpage.__contains__("http"): 
            webpage = "http://" + webpage
        webbrowser.open(webpage)


    elif command.__contains__("PY-"): # Run generated python scripts
        code = command.split("Please note that")[0].replace("\nPY-", "\n").split("PY-")[1]
        print(code)
        exec(code)


    elif command.__contains__("Search-"): # Search and run local programs
        search = command.replace("Search-", "")
        print("searching for " + search)
        windows_search(search)
        print("finished")


    elif command.__contains__("Type-"): # Type output into text box the user is in by simulating key presses
        typing = command[5:]
        send_string(typing)
        print("typing "+typing)


    elif command.__contains__("VBS-"):
        vbscode = command[4:].split("<NeWLiNe>")
        os.system("del vbs.vbs")
        # Delete the old vbs to prevent errors
        x=0
        while x<len(vbscode):
            os.system("echo "+vbscode[x]+">>vbs.vbs")
            x=x+1
        # Create the vbs
        os.system("vbs.vbs")
        # Run the vbs
        os.system("del vbs.vbs")
        # Delete the vbs
        # ONLY works in windows
        print("typing "+typing)

    elif (command.__contains__("LIST-")):
        iscom=1
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
        # FIX IT AGAIN TONY


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
        #try:
            noteid2 = noteid + 1
            notetochat = [f"the time is {datetime.datetime.now()}", f"my username is {os.environ.get('username')}"]
            if not overridechat:
                if not has_been_called:
                    with open('rules.txt', 'r') as f:
                        rules = f.read()
                    chatbot.ask(str(rules))
                    has_been_called = True
                thingy = chatbot.ask(prompt=str(f"{userinput},note {notetochat[noteid]}"))
                #for data in thingy:
                say(thingy)
                execute_command(command=thingy)

                    
            else:
                command = input()
            

        #except Exception as e:
        #   say("A error has occured")
        #    print("error")
        #    print(e)

    return command, noteid2