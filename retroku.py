"""
Grace Cox & Alex Chesin
Curses Test for RETROKU
Prints Sudoku board and given digits
"""
import curses
from curses import wrapper

ROWS = 9
COLS = 9


def highlight(scr, r, c, color):
    scr.chgat(*(cell_l(r, c)), 1, color | scr.inch(*(cell_l(r, c))))
    scr.chgat(*(cell(r, c)), 1, color | scr.inch(*(cell(r, c))))
    scr.chgat(*(cell_r(r, c)), 1, color | scr.inch(*(cell_r(r, c))))


def cell_l(r, c):
    if r not in range(1, ROWS + 1) or c not in range(1, COLS + 1):
        raise ValueError
    return 2 * r, 4 * c - 1


def cell(r, c):
    if r not in range(1, ROWS + 1) or c not in range(1, COLS + 1):
        raise ValueError
    return 2 * r, 4 * c


def cell_r(r, c):
    if r not in range(1, ROWS + 1) or c not in range(1, COLS + 1):
        raise ValueError
    return 2 * r, 4 * c + 1


def print_board(scr, template):
    with open(template, "r") as f:
        i = 0 #y position
        for line in f:
            scr.addstr(i, 0, line.strip("\n")) #print each line of template sans '\n'
            i += 1


def print_givens(scr, givens):
    if len(givens) > ROWS * COLS:
        raise ValueError
    givens = str(givens)
    i = 0 #index of number in givens
    for r in range(1, ROWS + 1):
        for c in range(1, COLS + 1):
            if i == len(givens): #break if index too high
                break
            if givens[i] in "123456789":
                scr.addch(*cell(r, c), givens[i], curses.A_BOLD)
            i += 1


def main(stdscr):
    # Clear screen
    stdscr.clear()
    #stdscr.bkgdset(curses.ACS_VLINE)
    print_board(stdscr, "retroku.txt")
    print_givens(stdscr, "235ug1153ug135104	0194857 09349742595287403958724")
    stdscr.refresh()
    stdscr.getkey()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    for i in range(3, 8):
        highlight(stdscr, 5, i, curses.color_pair(1))
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)