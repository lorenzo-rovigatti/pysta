'''
Created on 19 dic 2019

@author: lorenzo
'''

import asyncio
import curses
import time

UPDATE_DISTANCE_EVERY = 1

@asyncio.coroutine
def send_command(message, loop, win):
    reader, writer = yield from asyncio.open_connection('192.168.1.141', 8888, loop=loop)

    writer.write(message.encode())
    data = yield from reader.read(100)
    writer.close()
    
    win.clear()
    win.addstr(str(data.decode()), curses.color_pair(1))
    win.refresh()
    

def main(stdscr):
    # make calls to getkey() non blocking
    stdscr.nodelay(True)
    # disable the cursor
    curses.curs_set(False)
    # enable terminal colours
    curses.start_color()
    # define the status color pair
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    
    status_window = curses.newwin(1, curses.COLS - 1, 0, 0)
    distance_window = curses.newwin(1, curses.COLS - 1, 1, 0)
    
    loop = asyncio.get_event_loop()

    next_distance_time = time.time() + UPDATE_DISTANCE_EVERY
    try:
        while True:
            try:
                key = stdscr.getkey()
                
                command = False
                if key == "w":
                    command = "forward"
                elif key == "a":
                    command = "left"
                elif key == "d":
                    command = "right"
                elif key == "s":
                    command = "stop"
                elif key == "r":
                    command = "reverse"
                
                if command != False:
                    loop.run_until_complete(send_command(command, loop, status_window))
            except curses.error:
                if time.time() > next_distance_time:
                    next_distance_time = time.time() + UPDATE_DISTANCE_EVERY
                    loop.run_until_complete(send_command("distance", loop, distance_window))
    finally:
        loop.close()


curses.wrapper(main)
