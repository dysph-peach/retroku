"""
Grace Cox & Alex Chesin
Curses Test for RETROKU
Prints Sudoku board and given digits
"""
import curses
from curses import wrapper
from flask import *
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os, random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.getcwd() + "/instance/db.sqlite"
db = SQLAlchemy(app)

class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzz_disp = db.Column(db.String(81), nullable=False)
    puzz_answ = db.Column(db.String(81), nullable=False)
    board = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False) # 1 for easy, 2 for medium, 3 for hard
    puzzle_type = db.Column(db.Integer, nullable=False) # each number will b a different type of puzzle
    puzzle_name = db.Column(db.String, unique=True, nullable=False)
    puzzle_rules = db.Column(db.String)

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
    with open(template, "r", encoding="utf-8") as f:
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


def main(stdscr, puzzle):
    with app.app_context():
        # Clear screen
        stdscr.clear()
        #stdscr.bkgdset(curses.ACS_VLINE)   
        print_board(stdscr, puzzle.board)
        print_givens(stdscr, puzzle.puzz_disp)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        r = 5
        c = 3
        lr = 5
        lc = 3
        curr_puzz = puzzle.puzz_disp
        highlight(stdscr, r, c, curses.color_pair(1))
        while curr_puzz != puzzle.puzz_answ:
            stdscr.refresh()
            key = stdscr.getkey()
            if key == "KEY_UP":
                lr = r
                lc = c
                r -= 1
            elif key == "KEY_DOWN":
                lr = r
                lc = c
                r += 1
            elif key == "KEY_LEFT":
                lc = c
                lr = r
                c -= 1
            elif key == "KEY_RIGHT":
                lc = c
                lr = r
                c += 1
            else:
                curr_puzz = puzzle.puzz_answ
            
            highlight(stdscr, lr, lc, curses.color_pair(2))
            highlight(stdscr, r, c, curses.color_pair(1))
        
        stdscr.refresh()
        stdscr.getkey()


def menu(stdscr):
    with app.app_context():
        stdscr.clear()
        position = 0
        puzzles = Puzzle.query.all()
        i = 0
        puzzle_selected = False
        while puzzle_selected == False:
            for pzl in puzzles:
                stdscr.addstr(i, 0, pzl.puzzle_name)
                i += 2
            stdscr.refresh()
            key = stdscr.getkey()
            if key == "KEY_UP":
                if position > 0:
                    position -= 2
            elif key == "KEY_DOWN":
                if position < 2 * (len(puzzles) - 1):
                    position += 2
            elif key == " ":
                puzzle = position / 2
                puzzle += 1
                puzzle_selected = True
        wrapper(main, Puzzle.query.filter_by(id=puzzle).first())


wrapper(menu)