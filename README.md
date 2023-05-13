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