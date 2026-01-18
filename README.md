# Welcome to RETROKU 
A command-line interface for solving Sudokus.

* Database, menu screen, puzzle addition, and input handling - [Alex Chesin](https://github.com/DetectiveAlex12)
* Cell handling, board display, and all other features - [Grace Cox](https://github.com/dysph-peach)

## HOW TO RUN
After installing the retroku file, navigate into it and run retroku.py from the terminal. 
If the window is too small, the puzzle will not display. You must resize the window and try again.

## CONTROLS
|KEY       |ACTION                                       |
|----------|---------------------------------------------|
|`←` OR `j`|     left                                    |
|`↓` OR `k`|     down                                    |
|`↑` OR `l`|     up                                      |
|`→` OR `;`|     right                                   |
|`SPACE`   |     select                                  |
|          |                                             |
|`,` (`<`) |scroll left within a cell                    |
|`.` (`>`) |scroll right within a cell                   |
|          |                                             |
|`n`       |enter '<u>n</u>ormal' mode (full size digits)|
|`p`       |enter '<u>p</u>encil' mode (small digits)    |
|`h`       |enter '<u>h</u>ighlight' mode                |
|`c`       |switch <u>c</u>olors                         |
|          |                                             |
|`s`       |check <u>s</u>olution (quits if correct)     |

### HIGHLIGHT MODE
When in highlight mode, press space to highlight the selected cell. If the cell is already highlighted the current color, the highlight will be removed. If the current color is different from the selected color, the highlight will be overwritten by the selected color.

