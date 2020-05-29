import json
import threading
import sys
import os
import urllib
import subprocess
# any solutions?
subprocess.check_output(["pip", "install", "playsound"])
subprocess.check_output(["pip3", "install", "playsound"])
from playsound import playsound


def play():
    print("Playing music!")
    playsound("musictemp/music.mp3")
    os.remove("musictemp/music.mp3")
    os.rmdir("musictemp")


args = sys.argv
id = int()
if args[0] == "play":
    id = int(args[1])
    # Play music NOW
    request = urllib.request.urlopen("https://teammusic-tw.firebaseio.com/upload/text.json")
    data = json.load(request)
    musiclist = data.values()
    url = musiclist[id]["url"]
    os.mkdir("musictemp")
    urllib.request.urlretrieve(url, "musictemp/music.mp3")
    t = threading.Thread(target=play)
    t.start()
