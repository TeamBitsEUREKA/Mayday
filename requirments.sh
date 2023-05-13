echo "Check addons?"

echo "Check for missing py addons y/n"
read varname
if [$varname=="y"];then
pip install SpeechRecognition
pip install pyChatGPT
pip install pyaudio
pip install pyautogui
pip install revChatGPT
fi
echo "Checking for missing core files"
read varname
if [$varname=="y"];then
checkandfix("font.py")
checkandfix("data.json")
checkandfix("build.bat")
checkandfix("run.py")

checkandfix("havoc.py")
fi

checkandfix(file){
isfound=0
if test -e $file
then
isfound=1
fi
if [$isfound==0];then;echo "${file} is not found";fi
if [$isfound==0];then;if -e "${file}.bak";then;mv "${file}.bak" $file;fi;fi
}
read varname