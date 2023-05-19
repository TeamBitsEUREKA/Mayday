1. You do not need to provide your Gmail or other account information.
2. You will only be prompted with your access token available here: https://chat.openai.com/api/auth/session.
3. Conversation ID is not needed and has not been tested, it might not work, although a workaround has been implemented in case it does not. Do not expect ChatGPT to remember your messages from older instances.

# Mayday - The World's Most Semi-Advanced Neura Bot

Mayday is a semi-advanced AI voice assistant built on ChatGPT. It enables users to interact with their devices through voice commands. With Mayday, you can open web pages, execute commands, and run python scripts with just your voice.

# Capabilities

Mayday provides access to the following functions:

   1. Chat with ChatGPT using speech recognition and Microsoft Bob.
   2. Open web pages with simple queries such as, "Mayday, open a video streaming website."
   3. Create, edit, and manage files and system applications through voice commands such as, "Mayday, create a text file on my desktop."
   4. Run ChatGPT generated one-liner python scripts such as , "Mayday, make a sound out of my speakers using python."
   5. Search for system-wide applications and files using your voice, "Mayday, search locally for Firefox."

# How it works

Mayday uses the unofficial python wrapper for ChatGPT and logs in using your ChatGPT account on startup. When you make a voice request, Mayday sends the text after the catchphrase to the ChatGPT engine. The engine is preconfigured to respond to your request based on the ruleset outlined in the quick start guide.

The response from ChatGPT is then checked for the necessary parameters to execute the command. If the response includes "Say-," for example, the say function is executed, and the details are obtained from the rest of the response.

The entire program relies on ChatGPT, which can be advantageous. If you provide a vague argument, ChatGPT will do its best to understand what you mean and deliver a good result. For instance, if you say "search the system for a web browser," it might output "SEARCH-Chrome," which would find and launch Chrome, even if you didn't mention the specific name of the browser.

Some things to note:
1. ChatGPT will remember what you said if you specified a conversation ID, even after a full restart; meaning that if you have a preferance it will remember it.
2. ChatGPT has acess to local Command line, meaning it can cause damage if you are not carefull, although if you tell it to do something like delete system32 it will tell you that that is a bad idea, and not execute the command.

# How to install

## setting up the tortoise-tts-fast TTS engine along with Mayday:
Before starting, I would like to give propts to @155234H for making a faster version of base tortoise-tts made by @neonbjb. I congradulate everybody that has worked on that TTS project and hope they have good luck writing their papers. you can find both the base version of tortoise-tts and the modified faster version that this repo uses below:
https://github.com/neonbjb/tortoise-tts
https://github.com/152334H/tortoise-tts-fast

to download the requirments for the TTS engine, you can run the commands as follows:

1. Download and install anaconda, as this repo fully supports it and it is recommended if you dont want to hop through alot of hoops to install the requirments on the latest version of python, you can find the anaconda installer here: https://www.anaconda.com/ once you have installed anaconda launch Anaconda prompt (on windows you can search it, you should be able to install this without anaconda on linux, although this is not tested), every command we are going to be running is going to be inside of Anaconda prompt so dont mess this up.
2. cd to the directory you want to use for this project (optional)
3. run 'git clone -b Switch-TTS-Engine https://github.com/TeamBitsEUREKA/Mayday.git'
4. cd into the directory 'cd Switch-TTS-Engine'
5. git clone the TTS engine 'git clone https://github.com/152334H/tortoise-tts-fast'
6. cd into the TTS engine 'cd tortoise-tts-fast'
7. install TTS engine requirments 'pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117'
8. install the TTS engine 'python -m pip install -e .' ('python3 -m pip install -e .' for Linux users)
9. install BigVGAN incoder 'pip3 install git+https://github.com/152334H/BigVGAN.git'
10. cd back to the main directory 'cd ..'
11. delete the TTS engine directory 'rmdir /s tortoise-tts-fast' press 'y' when prompted
12. open the 'havoc.py' file using a text editor, and at the top of the file you should see the following:
```
#config
ttslogs=True
usegoogletts=False
usetortousetts=False
sayoutput=True
```
modify it to look like this (if you want to use the best TTS engine available to the program)
```
#config
ttslogs=True
usegoogletts=False
usetortousetts=True
sayoutput=True
```
13. save your changes and exit out of your text editor
14. finally, run the program 'python run.py'
