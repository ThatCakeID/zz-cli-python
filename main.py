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
for k, v in musics.items():
    list_of_musics.append(v)

# Initialize Curses
s = curses.initscr()
curses.noecho()
curses.cbreak()
s.keypad(True)


def toast(text, screen, rows, cols):
    # Draws a toast
    s.attron(curses.color_pair(3))
    screen.addstr(int(rows / 2) - 2, int((cols / 2) - len(text) / 2), " " * (len(text) + 4))
    screen.addstr(int(rows / 2) - 2, int(cols / 2), "(!)")
    s.attroff(curses.color_pair(3))
    s.attron(curses.color_pair(1))
    screen.addstr(int(rows / 2) - 1, int((cols / 2) - len(text) / 2), " " * (len(text) + 4))
    screen.addstr(int(rows / 2), int((cols / 2) - len(text) / 2), "  " + text + "  ")
    screen.addstr(int(rows / 2) + 1, int((cols / 2) - len(text) / 2), " " * (len(text) + 4))

    # Toast will close if you press anything
    screen.getch()
    s.attroff(curses.color_pair(1))


def flexadd(y, x, text):
    screen = curses.initscr()
    rows, cols = screen.getmaxyx()
    cols -= 1
    splitted = [text[i:i+cols] for i in range(0, len(text), cols)]
    for i, txt in enumerate(splitted):
        s.addstr(y+i, x, txt)


def main(s):
    # used to cycle between screens
    screen_index = 1
    screens = ["Help", "Home", "Info"]
    selected = 1
    screen = "Home"
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    while 1:
        screen = screens[screen_index]

        s = curses.initscr()
        # Clear screen
        s.clear()
        curses.curs_set(0)
        rows, cols = s.getmaxyx()

        s.attron(curses.color_pair(1))
        # Draw TeamMusic Header
        s.addstr(0, 0, " " * (int(cols / 2) - (int(len("ZryteZene - " + screen) / 2))) + "ZryteZene - " + screen + " " * (
                    int(cols / 2) - (int(len("ZryteZene - " + screen) / 2))))
        s.addstr(1, 0, " " * cols)

        s.attroff(curses.color_pair(1))

        if screen == "Home":
            s.attron(curses.color_pair(2))
            s.addstr(3, 0, "Latest Musics:")
            s.attroff(curses.color_pair(2))
            s.attron(curses.color_pair(1))
            s.addstr(rows - 1, 0, " " * (cols - 1))
            s.addstr(rows - 1, 0, "RIGHT AND LEFT KEY: CYCLE BETWEEN SCREENS")
            s.attroff(curses.color_pair(1))
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
                    s.addstr(musicpos, 0, " " + str(musicpos-3) + ". " + musicname, curses.A_STANDOUT)
                else:
                    s.addstr(musicpos, 0, " " + str(musicpos - 3) + ". " + musicname)

            s.refresh()
            key = s.getch()
            if key == curses.KEY_DOWN:
                if not selected >= len(list_of_musics):
                    selected += 1
                else:
                    curses.beep()
            elif key == curses.KEY_UP:
                if not selected <= 1:
                    selected -= 1
                else:
                    curses.beep()
            elif key == curses.KEY_LEFT:
                if screen_index != 0:
                    screen_index -= 1
                else:
                    curses.beep()
                    toast("No Screen after this", s, rows, cols)
            elif key == curses.KEY_RIGHT:
                if screen_index != len(screens):
                    screen_index += 1
                else:
                    curses.beep()
                    toast("No Screen after this", s, rows, cols)
            elif key == 27:
                curses.endwin()
                exit(0)

        elif screen == "Help":
            s.attron(curses.color_pair(1))
            s.addstr(rows - 1, 0, " " * (cols - 1))
            s.addstr(rows - 1, 0, "LEFT ARROW KEY: GET BACK")
            s.attroff(curses.color_pair(1))
            s.addstr(3, 0, " TeamMusic CLI Help")
            flexadd(5, 0, "LEFT ARROW AND RIGHT ARROW KEY : CYCLE TROUGH SCREENS")

            s.refresh()
            key = s.getch()
            if key == curses.KEY_LEFT:
                if screen_index != 0:
                    screen_index -= 1
                else:
                    curses.beep()
                    toast("No Screen after this", s, rows, cols)
            elif key == curses.KEY_RIGHT:
                if screen_index != len(screens):
                    screen_index += 1
                else:
                    curses.beep()
                    toast("No Screen after this", s, rows, cols)

        elif screen == "info":
            flexadd(3, 0, " ZryteZene is a free music streaming service built in Firebase")
            s.refresh()
            key = s.getch()
            if key == curses.KEY_LEFT:
                if screen_index != 0:
                    screen_index -= 1
                else:
                    curses.beep()
                    toast("No Screen after this", s, rows, cols)
            elif key == curses.KEY_RIGHT:
                if screen_index != len(screens):
                    screen_index += 1
                else:
                    curses.beep()
                    toast("No Screen after this", s, rows, cols)

            s.getkey()


curses.wrapper(main)
