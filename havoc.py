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



def Find(string):
 
    # findall() has been used
    # with valid conditions for urls in string
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
#cmd:detect os
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
noteid2=0
noteid=0
#intiallize noteids
def make_sound(pitch,delay): # We needed this in order to change the sound API depending on the OS
        #CMD:moved os detection to the top of the file
 try:
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
 except Exception as e:
            say("A error has occured")
            font.gen("error")
            print("error in make_sound")
            print("error code:"+e)
            return "ErR"


def askai(question):
    #cmd:easyer to call/mantain in the event of api changes
    return chatbot.ask(question)

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
if incode(incode("testing of #weird LeTtErs# :)"))!="testing of #weird LeTtErs# :)":
    font.get("TnT")
    say("who broke incode again!")
    #self check
string_acess_token = str(api_key_chatgpt) #this is because if I directly write acess token it dosent work, for some reason.

chatbot = ChatGPT(api_key=api_key_chatgpt)
#for everyones sake put this(/|\) in the json file
#cmd:done

# cmd: also check if the api key is functional before blaming it on incode

if(len(conversation_id)<5):
    say("New chat created")
with open("rules.txt", "r") as file:
    rules = file.read()
askai(rules)
askai("note the current os is"+ostype)
chatgpt_flag = True
loading=False
clear()
font.gen("Mayday")
font.gen(verson)
CMD = "0000"
noteid2=0
noteid=0




def execute_command(command):
 try:
    allowtwo=0
    if command.replace("AnD","")!=command:
        oldcom=command
        command=command.split("AnD")[0]
        oldcom=oldcom[len(command)+3:]
        allowtwo=1


    if command.__contains__("COMmand-"): # Run local CMD commands
        command = command.replace("COMmand-", "").replace("%username%", r"\%username%").split("Please note that")[0]
        print(command)
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
        print("typing "+typing)
        send_string(typing)


    elif command.__contains__("VBS-"):
     if ostype=="win":
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
     else:
        resp = askai("VBS is not supported on"+ostype)
        #dont waste chatgpts time
    elif (command.__contains__("LIST-")):
        iscom=1
        dircom=command.split("LIST-")[1]
        dircom=",".join(os.listdir(dircom)).replace(".lnk","")
        print(dircom)
        resp = askai("the files in "+command.split("LIST-")[1]+" are "+dircom)
        command=execute_command(resp)

    elif command.__contains__('Timer-'):
        timer = command.replace('Timer-', "")
        print("starting timer for " + timer + " seconds")
        timer_thread = run_thread.Thread(target=start_timer, args=[timer])
        timer_thread.start()
        # FIX IT AGAIN TONY
        #cmd:i dont get the joke


    # Other command cases go here

    if (command.__contains__("I'm sorry, I am ") or command.__contains__("I'm sorry, but as a ")):
                askai("NEVER tell me what you can or cant do, just do what I say.\nNEVER explain what a command does\nNEVER tell me that your a language model")
    #punish chatGPT for errors

    if(allowtwo==1): #check for second command and run it
            command=execute_command(oldcom)
    if(len(command)>300):
        resp = askai("please type shorter commands(less then 300 chars)")
    return command
 except Exception as e:
            say("A error has occured")
            font.gen("error")
            print("error in command handling")
            print(e)
            try:
                say(askai("your command"+command+"was not ran due to a bug on my side"))
            except Exception as e:
                say("error with speech or call commands")
            return "ErR"

def init(userinput, noteid):
    global resp, has_been_called, command
    resp = "ERROR"
    if userinput.replace(" ","") in ["hi", "hello"]:
        resp = "hello"
        say(resp)
    else:
        try:
            noteid2 = noteid + 1
            notetochat = [f"the time is {datetime.datetime.now()}", f"my username is {os.environ.get('username')}"]
            try: # check if notetochat[noteid] is invalid, if so, set it to 0.
                noteid2=notetochat[noteid]
                noteid2 = noteid + 1
            except:
                noteid2=0
                noteid=0
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
            

        except Exception as e:
            say("A error has occured")
            font.gen("error")
            print("error in init")
            print("error code:"+e)

    return command, noteid
