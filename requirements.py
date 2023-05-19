import os
os.system('git clone git clone https://github.com/152334H/tortoise-tts-fast')
os.chdir('tortoise-tts-fast')
os.system('pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117')
os.system('python3 -m pip install -e .')
os.chdir('..')
os.system('rm -rf tortoise-tts-fast')