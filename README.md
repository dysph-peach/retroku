Welcome to RETROKU, a command-line interface for solving Sudokus.

Database, menu screen, puzzle addition, and input handling - Alex Chesin
Cell handling, board display, and all other features - Grace Cox

HOW TO RUN:
    After installing the retroku file, navigate into it and run retroku.py from the terminal. 
    If the window is too small, the puzzle will not display. You must resize the window and try again.

CONTROLS:
    '←' OR 'j':     left
    '↓' OR 'k':     down
    '↑' OR 'l':     up
    '→' OR ';':     right
    SPACE:          select

    ',' (<):        scroll left within a cell
    '.' (>):        scroll right within a cell

    'n':            switch to 'normal' mode (full size digits)
    'p':            switch to 'pencil' mode (small digits)
    'h':            switch to 'highlight' mode
    'c':            switch colors

    's':            check solution. Quits if correct.

HIGHLIGHT MODE:
    When in highlight mode, press space to highlight the selected cell. If the cell is already highlighted 
    the current color, the highlight will be removed. If the current color is different from the selected
    color, the highlight will be overwritten by the selected color.

