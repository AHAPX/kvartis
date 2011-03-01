import curses, sys
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
while 1:
    if stdscr.getch() == 266:
        curses.reset_shell_mode();
        sys.exit()
    print '1'
#    stdscr.addstr(str(stdscr.getch())+" ")
