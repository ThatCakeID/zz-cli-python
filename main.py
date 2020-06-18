import curses
import json
import pygame       # YES I USE PYGAME WHY NOT
import requests
import time

# Init pygame for playing music
pygame.init()

musics = dict()
list_of_musics = list()
# get request to teammusic database
r = requests.get("https://teammusic-tw.firebaseio.com/upload/text.json")

# Detect if status code is not okay
if r.status_code != 200:
    print("Response error")
    exit(1)

# loads data
musics = json.loads(r.text)
for k, v in musics.items():
    list_of_musics.append(v)

# Initialize Curses
s = curses.initscr()
curses.noecho()
curses.cbreak()
s.keypad(True)


def main(s):
    selected = 1
    screen = "home"
    frames = 0
    lasttime = 0
    fps = 0
    while 1:
<<<<<<< HEAD
        frames += 1
        if screen == "home":
            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
            s = curses.initscr()
            # Clear screen
            s.clear()
            curses.curs_set(0)
            rows, cols = s.getmaxyx()

            s.attron(curses.color_pair(1))
            # Draw TeamMusic
            s.addstr(0, 0, " " * (int(cols/2)-(int(len("TeamMusic") / 2))) + "TeamMusic" + " " * (int(cols/2) - (int(len("TeamMusic") / 2))))
            s.addstr(0, 0, "FPS: " + str(fps))
            s.addstr(1, 0, " " * cols)
            s.addstr(rows-1, 0, " " * (cols-1))
            s.addstr(rows - 1, 0, "H: SHOWS HELP MANUAL")
            s.attroff(curses.color_pair(1))

            s.attron(curses.color_pair(2))
            s.addstr(3, 0, "Latest Musics:")
            s.attron(curses.color_pair(2))

            # Draw the musics
            musicpos = 3
            for music in list_of_musics:
                if musicpos == rows - 3:
                    break
                musicpos += 1
                musicname = music["name"]
                if cols <= len(musicname):
                    musicname = musicname[:len(musicname) - (len(musicname)-cols-2)]

                if selected == (musicpos-3):
                    s.attron(curses.color_pair(1))
                s.addstr(musicpos, 0, " " + str(musicpos-3) + ". " + musicname)
                if selected == (musicpos-3):
                    s.attroff(curses.color_pair(1))

            key = s.getch()
            if key == curses.KEY_DOWN and not selected >= len(list_of_musics):
                selected += 1
            elif key == curses.KEY_UP and not selected <= 0:
                selected -= 1

            s.refresh()
            s.getch()

        if lasttime != int(time.time()):
            lasttime += 1
            fps = frames
            frames = 0
=======
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        s = curses.initscr()
        # Clear screen
        s.clear()
        curses.curs_set(0)
        rows, cols = s.getmaxyx()

        s.attron(curses.color_pair(1))
        # Draw TeamMusic
        s.addstr(0, 0, " " * (int(cols/2)-(int(len("TeamMusic") / 2))) + "TeamMusic CLI" + " " * (int(cols/2) - (int(len("TeamMusic") / 2))))
        s.addstr(1, 0, " " * cols)
        s.attroff(curses.color_pair(1))

        s.attron(curses.color_pair(2))
        s.addstr(3, 0, "Latest Musics:")
        s.attron(curses.color_pair(2))

        # Draw the musics
        musicpos = 3
        for music in list_of_musics:
            if musicpos == rows - 3:
                break
            musicpos += 1
            musicname = music["name"]
            if cols <= len(musicname):
                musicname = musicname[:len(musicname) - (len(musicname)-cols-2)]
            s.addstr(musicpos, 0, " " + str(musicpos-2) + ". " + musicname)

        key = s.getch()
        if key == curses.KEY_DOWN:
            selected += 1

        s.refresh()
        s.getch()
>>>>>>> 3c75de2cbe38a7ce325c90a208d538178fece63c


curses.wrapper(main)
