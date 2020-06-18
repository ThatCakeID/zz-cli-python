from curses import wrapper
import curses
import json
import pygame       # YES I USE PYGAME WHY NOT
import requests

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
list_of_musics = musics.itervalues()

# Initialize Curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)


def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 11):
        v = i-10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    stdscr.refresh()
    stdscr.getkey()


wrapper(main)
