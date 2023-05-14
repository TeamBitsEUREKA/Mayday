import os
import threading
import tkinter as tk
from tkinter import messagebox

from havoc import init, get_password_and_gmail, say, make_sound
import speech_recognition as sr
import font
import sys
import json

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("MAYDAY")
        self.start_button = tk.Button(self.window, text="Start", command=self.start)
        self.start_button.pack(pady=10)
        
        self.settings_button = tk.Button(self.window, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=10)
        
        self.mic_button = tk.Button(self.window, text="Direct Input", command=self.direct_input)
        self.mic_button.pack(pady=10)

        self.output_text = tk.Text(self.window)
        self.output_text.pack()

    def direct_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ""
            try:
                said = r.recognize_google(audio)
            except Exception as e:
                print("Exception: " + str(e))
            text = said.lower()
            self.output_text.insert(tk.END, text + '\n')


    def save_settings(self):
        wakes = self.wake_entry.get().split(',')
        setup_commands = self.setup_entry.get().split(',')

        data = {
            "wakes": wakes,
            "setup": setup_commands[0],
            "setup2": setup_commands[1] if len(setup_commands) > 1 else ""
        }

        with open('settings.json', 'w') as f:
            json.dump(data, f)

        self.settings_window.destroy()



    def open_settings(self):
        self.settings_window = tk.Toplevel(self.window)
        self.settings_window.title("Settings")

        self.wake_label = tk.Label(self.settings_window, text="Wake Words (comma separated):")
        self.wake_label.pack()

        self.wake_entry = tk.Entry(self.settings_window)
        self.wake_entry.pack()

        self.setup_label = tk.Label(self.settings_window, text="Setup Commands (comma separated):")
        self.setup_label.pack()

        self.setup_entry = tk.Entry(self.settings_window)
        self.setup_entry.pack()

        self.save_button = tk.Button(self.settings_window, text="Save", command=self.save_settings)
        self.save_button.pack()



    def start(self):
        self.thread = threading.Thread(target=self.run_program)
        self.thread.start()
        self.start_button.config(text="Stop", command=self.stop)

    def stop(self):
        self.window.destroy()

    def run_program(self):
        global overridechat, wakes, setup, setup2
        overridechat=False
        def get_audio():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
                said = ""
                try:
                    said = r.recognize_google(audio)
                except Exception as e:
                    print("Exception: " + str(e))
            return said.lower()

        SHUTDOWN = "process exit"

        def get_settings():
            default_data = {
                "wakes": ["mayday", "panpan"],
                "setup": "how setup",
                "setup2": "how set up"
            }

            try:
                with open('settings.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                # File does not exist, return default data
                return default_data

            # File exists, return data from the file
            return data["wakes"], data["setup"], data["setup2"]

        wakes, setup, setup2 = get_settings()

        self.output_text.insert(tk.END, f"wakes = {wakes}\n")
        self.output_text.insert(tk.END, f"setup = {setup}\n")
        self.output_text.insert(tk.END, f"setup2 = {setup2}\n")

        exited=0
        noteid=0
        while True:
            try:
                print("Listening")
                if(overridechat==False):
                    text = get_audio().lower()
                else:
                    text=input()
                x=0
                if(text==setup or text==setup2):
                    make_sound(200,10)
                    make_sound(150,10)
                    make_sound(100,10)
                    make_sound(50,10)
                    
                    say("are you sure?")
                    font.gen("Y / N")
                    text = get_audio()
                    text=text.replace("i am ","im ")
                    text=text.replace("im ","i ")
                    text=text.replace("i sure","")
                    text=text.replace("sure","y")
                    text=text.replace("yes","y")
                    text=text.replace("no","n")
                    text=text.replace("dont","n")
                    if(text=="y"):
                        os.system("del /f data.json")
                        get_password_and_gmail()
                while(x<len(wakes)):
                    WAKE=wakes[x]
                    x=x+1
                    if text.startswith(WAKE):
                        if text==WAKE:
                            print ("detecting:")
                            make_sound(500,200)
                            if(overridechat==False):
                                text = get_audio().lower()
                            else:
                                text=input()
                        elif text.startswith(WAKE):
                            text=text.split(WAKE)[1]
                        resp,noteid=init(text,noteid)
                if text.count(SHUTDOWN) > 0:
                    make_sound(500,200)
                    make_sound(200,200)
                    exited=1
                    exit()
                print(text)
            except Exception as e:
                font.gen("error")
                print(e)
                os.execv(sys.executable, [sys.executable] + sys.argv)


    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()

