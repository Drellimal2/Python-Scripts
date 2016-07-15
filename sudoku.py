# -*- coding: utf-8 -*-
"""
Created on Thu Apr 07 08:27:19 2016

@author: Dane
"""
changes = []
board = [[] for x in range(9)]

def print_board(board):
    for row in range(len(board)):
        line = board[row]
        new_line = []
        
        for col in range(len(line)):
            val = line[col]
            if type(val) == type(set([])):
                new_line += ["."]
            else:
                new_line += [str(val)]
        print " ".join(new_line)
    
"""
    Miss Functions
    Returns what is missing in rows, columns and sections
"""
def row_miss(line):
    u_limit = len(line) + 1 
    nums = set([y for y in range(1,u_limit)])
    for val in line:
        if type(val) == type(3):
            nums.remove(val)
    return nums 

def col_miss(board, x):
    u_limit = len(board) + 1
    nums = set([y for y in range(1,u_limit)])
    for row in board:
        item = row[x]
        if type(item) == type(3):
            if item in nums:
                nums.remove(item)
    return nums

def sec_miss(board, x):
    row = (x / 3) + 1
    col = (x % 3) + 1
    row *= 3
    col *= 3
    
    sec = [line[col-3:col] for line in board[row-3:row]]
    nums = set([y for y in range(1,10)])
    for x in range(len(sec[0])):
        for row in sec:
            item = row[x]
            if type(item) == type(3):
                if item in nums:
                    nums.remove(item)
    return nums



"""
    Gets the section based on row and column.
    Sections are:-
    0 1 2
    3 4 5
    6 7 8
"""
def get_sec(row, col):
    sec = (row/3) * 3 + col/3
    return sec

"""
    Fix Functions
    Updates(fixes) the affected row, column and section 
    when space is updated.
"""
def fix_row(board, row, val):
    for x in range(len(board[row])):
        if type(board[row][x]) == type(set([])):
            board[row][x] = board[row][x] -set([val])

def fix_col(board, col, val):
    for x in range(len(board)):
        if type(board[x][col]) == type(set([])):
            if val in board[x][col]:
                board[x][col] = board[x][col] - set([val])

                
def fix_sec(board, sec, val):
    row = (sec / 3) + 1
    col = (sec % 3) + 1
    row *= 3
    col *= 3
    for x in range(col-3, col):
        for y in range(row-3, row):
            if type(board[y][x]) == type(set([])):
                if val in board[y][x]:
                    board[y][x] = board[y][x] - set([val])    

    
def fix_all(board, row, col, val, place):
    sec = get_sec(row, col)
    fix_row(board, row, val)
    fix_col(board, col, val)
    fix_sec(board, sec, val)
    
    
"""
    Fill Functions
    Updates the board.
"""
def fill_rows(board, row):
    missing = row_miss(board[row])
    for x in range(len(board[row])):
        if type(board[row][x]) == type(set([])):
            if len(missing) == 1:
                board[row][x] = missing.pop()
                fix_all(board, row, x, board[row][x], 1)
                break
            elif len(board[row][x]) == 0:            
                board[row][x] = missing
            else:
                board[row][x] = board[row][x].intersection(missing)
                if len(board[row][x]) == 1:
                    board[row][x] = board[row][x].pop()
                    fix_all(board, row, x, board[row][x], 1)

                
def fill_cols(board, col):
    missing = col_miss(board, col)
    for x in range(len(board)):
        if type(board[x][col]) == type(set([])):
            if len(missing) == 1:
                board[x][col] = missing.pop()
                fix_all(board, x, col, board[x][col],2)
                break
            elif len(board[x][col]) == 0:            
                board[x][col] = missing
            else:
                board[x][col] = board[x][col].intersection(missing)
                if len(board[x][col]) == 1:
                    board[x][col] = board[x][col].pop()
                    fix_all(board, x, col, board[x][col],2)    

def fill_sec(board, sec):
    row = (sec / 3) + 1
    col = (sec % 3) + 1
    row *= 3
    col *= 3
    
    missing = sec_miss(board, sec)
    for x in range(col-3, col):
        for y in range(row-3, row):
            if type(board[y][x]) == type(set([])):
                if len(missing) == 1:
                    board[y][x] = missing.pop()
                    fix_all(board, y, x, board[y][x],3)
                    break
                elif len(board[y][x]) == 0:            
                    board[y][x] = missing
                else:
                    board[y][x] = board[y][x].intersection(missing)
                    if len(board[y][x]) == 1:
                        board[y][x] = board[y][x].pop()
                        fix_all(board, y, x, board[y][x],3)
                        
                


def fine_tune_row(board):
    for x in range(len(board)):
        choices = []        
        for y in board[x]:
            if type(y) == type(set([])):
                choices += list(y)
        
        for y in range(len(board[x])):
            if type(board[x][y]) == type(set([])):
#                choice = -1

                for w in board[x][y]:
                    if choices.count(w) == 1:
                        board[x][y] = w
                        fix_all(board, x, y, board[x][y], 4)
#                        choice = w
                        break
#                if choice > -1:
#                    board[x][y] = choice
#                    fix_all(board, x, y, board[x][y], 4)
                    
def fine_tune_col(board):
    for x in range(len(board[0])):
        choices = []
        bboard = [board[y][x] for y in range(len(board))]
        for y in bboard:
            if type(y) == type(set([])):
                choices += list(y)
        for z in range(len(board)):
            if type(board[z][x]) == type(set([])):
                for w in board[z][x]:
                    if choices.count(w) == 1:
                        board[z][x] = w
                        fix_all(board, z, x, board[z][x], 4)
                        break

def fine_tune_sec(board):
    for sec in range(9):
        choices = []
        row = (sec / 3) + 1
        col = (sec % 3) + 1
        row *= 3
        col *= 3
        for x in range(col-3, col):
            for y in range(row-3, row):
                if type(board[y][x]) == type(set([])):
                    choices += list(board[y][x])
        for x in range(col-3, col):
            for y in range(row-3, row):
                if type(board[y][x]) == type(set([])):
                    for z in board[y][x]:
                        if choices.count(z) == 1:
                            board[y][x] = z
                            fix_all(board, y, x, board[y][x],3)

def sec_row_fix(board, row, sec, val):
    for x in range(len(board[row])):
        if get_sec(row, x) != sec:
            if type(board[row][x]) == type(set([])):
                board[row][x] = board[row][x] - set([val])

def sec_col_fix(board, col, sec, val):
    for row in range(len(board)):
        if get_sec(row, col) != sec:
            if type(board[row][col]) == type(set([])):
                board[row][col] = board[row][col] - set([val])
   
        
def col_sec_fix(board, col, sec, val):
    row = (sec / 3) + 1
    col1 = (sec % 3) + 1
    row *= 3
    col1 *= 3
    for c in range(col1-3, col1):
        for r in range(row-3, row):
            if c == col:
                break
            else:
                if type(board[r][c]) == type(set([])):
                    board[r][c] -= set([val])
                
def row_sec_fix(board, row, sec, val):
    row1 = (sec / 3) + 1
    col = (sec % 3) + 1
    row1 *= 3
    col *= 3
    for r in range(row1-3, row1):
        for c in range(col-3, col):
            if r == row:
                break
            else:
                if type(board[r][c]) == type(set([])):
                    board[r][c] -= set([val])    
    
    
def sec_row(board, sec):
    choices = [[],[],[]]
    row = (sec / 3) + 1
    col = (sec % 3) + 1
    row *= 3
    col *= 3
    full_choices = []
    for x in range(col-3, col):
        for y in range(row-3, row):
            
            if type(board[y][x]) == type(set([])):
                choices[y-(row-3)] += list(board[y][x])
                full_choices += list(board[y][x])
    for n in range(len(choices)):
        choice = set(choices[n])
        for x in choice:
            if x not in choices[(n+1)%3] and x not in choices[(n+2)%3]:
                sec_row_fix(board,row+n-3, sec, x)

def finer_tune_row_fix(board, row, x):
    for col in range(len(board[row])):
        if type(board[row][col]) == type(set([])):
            if board[row][col] != x:
                board[row][col] -= x

def finer_tune_col_fix(board, col, x):
    for row in range(len(board)):
        if type(board[row][col]) == type(set([])):
            if board[row][col] != x:
                board[row][col] -= x                

def finer_tune_sec_fix(board, sec, val):                   
    row = (sec / 3) + 1
    col = (sec % 3) + 1
    row *= 3
    col *= 3
    for x in range(col-3, col):
        for y in range(row-3, row):
            if type(board[y][x]) == type(set([])):
                if board[y][x] != val:
                    board[y][x] -= val
                    
def finer_tune_row(board, row):
    for val in board[row]:
        if type(val) == type(set([])):
            if board[row].count(val) == len(val):
                finer_tune_row_fix(board, row, val)

def finer_tune_col(board, col):
        bboard = [board[y][col] for y in range(len(board))]
        for y in bboard:
            if type(y) == type(set([])):
                if bboard.count(y) == len(y):
                    finer_tune_col_fix(board, col, y)

def sec_count(board, sec, val):
    count = 0
    row = (sec / 3) + 1
    col = (sec % 3) + 1
    row *= 3
    col *= 3
    for x in range(col-3, col):
        for y in range(row-3, row):
            if type(board[y][x]) == type(set([])):
                if board[y][x] == val:
                    count += 1
    return count
    
def finer_tune_sec(board):
    for sec in range(9):
        row = (sec / 3) + 1
        col = (sec % 3) + 1
        row *= 3
        col *= 3
        for x in range(col-3, col):
            for y in range(row-3, row):
                if type(board[y][x]) == type(set([])):
                    if sec_count(board, sec, board[y][x] ) == len(board[y][x]):
                        finer_tune_sec_fix(board, sec, board[y][x])
                    
def sec_col(board, sec):
    choices = [[],[],[]]
    row = (sec / 3) + 1
    col = (sec % 3) + 1
    row *= 3
    col *= 3
    full_choices = []
    for x in range(col-3, col):
        for y in range(row-3, row):
            
            if type(board[y][x]) == type(set([])):
                choices[x-(col-3)] += list(board[y][x])
                full_choices += list(board[y][x])
    for n in range(len(choices)):
        choice = set(choices[n])
        for x in choice:
            if x not in choices[(n+1)%3] and x not in choices[(n+2)%3]:
                sec_col_fix(board,col+n-3, sec, x)
#    


def col_sec(board, col):
    choices = [[],[],[]]
    rows = len(board)
    secs = []
    for row in range(rows):
        sec = get_sec(row, col)
        if sec not in secs:
            secs.append(sec)
        if type(board[row][col]) == type(set([])):
            choices[row/3] += list(board[row][col])
    for n in range(len(choices)):
        choice = set(choices[n])
        for x in choice:
            if x not in choices[(n+1)%3] and x not in choices[(n+2)%3]:
                col_sec_fix(board,col, secs[n], x)

def row_sec(board, row):
    choices = [[],[],[]]
    cols = len(board[row])
    changed = []
    secs = []
    for col in range(cols):
        sec = get_sec(row, col)
        if sec not in secs:
            secs.append(sec)
        if type(board[row][col]) == type(set([])):
            choices[col/3] += list(board[row][col])
    for n in range(len(choices)):
        choice = set(choices[n])
        for x in choice:
            
            if x not in choices[(n+1)%3] and x not in choices[(n+2)%3]:
                row_sec_fix(board,row, secs[n], x)
                changed.append(x)
#    if len(changed) > 1:
#        if len(changed) == 2:
#            for x in changed:
#                a= [x for y in choices for x in y]
#                if a.count == 2:
                    

for z in range(len(board)):
    x = raw_input()
    for y in x:
        if y == '0':
            board[z].append(set([]))
        else:
            board[z].append(int(y))
            
print_board(board)

def basic():
    for x in range(9):
        fill_rows(board, x)
        fill_cols(board, x)
        fill_sec(board, x)
        
print("\n\n")



        #fine_tune_row(board)
for y in range(200):
    basic()
    fine_tune_row(board)
    fine_tune_col(board)
    fine_tune_sec(board)
    finer_tune_sec(board)
    for xy in range(9):
        finer_tune_row(board, xy)
        finer_tune_col(board, xy)
        sec_row(board, xy)
        col_sec(board, xy)
        row_sec(board, xy)
        sec_col(board, xy)
    

print "\n\n SOLUTION"    
print_board(board)

    
for row in board:
    print str(row)



#print "\n".join(options)

#print col_miss(board,2)
#board[0][5] = []
#print row_miss(board[0])
#print sec_miss([line[3:6] for line in board[3:6]])

# CHECKER METHODS
def check_secs(board):
    for x in range(9):
        row = (x / 3) + 1
        col = (x % 3) + 1
        row *= 3
        col *= 3
        
        sec = [line[col-3:col] for line in board[row-3:row]]
        for line in sec:
            print line
        print "\n"

def check_rows(board):
    for row in board:
        nums = set([x for x in range(1,10)])
        for item in row:
            if type(item) == type(3):
                if item in nums:
                    nums.remove(item)
                else:
                    return False
    return True
    
def check_cols(board):
    for x in range(len(board[0])):
        nums = set([y for y in range(1,10)])
        for row in board:
            item = row[x]
            if type(item) == type(3):
                if item in nums:
                    nums.remove(item)
                else:
                    return False
    return True
def check_sec(sec):
    nums = set([y for y in range(1,10)])
    for x in range(len(board[0])):
        for row in board:
            item = row[x]
            if type(item) == type(3):
                if item in nums:
                    nums.remove(item)
                else:
                    return False
    return True

def num_row_missing(board, num):
    missing = []
    for x in range(len(board)):
        if num not in board[x]:
            missing.append(x)
    return missing

def num_col_missing(board, num):
    missing = []
    for x in range(len(board)):
        bboard = [board[y][x] for y in range(len(board))]
        if num not in bboard:
            missing.append(x)
    return missing

#def only_row(board)
    
"""

EXPERT
670040001
900030704
000607900
100070000
000300409
403901200
007000530
000008000
010050698

005280000
000004100
009000403
900700060
080010040
050009001
406000200
007400000
000025600

 SOLUTION
. 4 5 2 8 . 7 9 6
. . . . . 4 1 . .
. . 9 . . . 4 . 3
9 . . 7 . . 5 6 .
6 8 . 5 1 . 9 4 7
7 5 . . . 9 . . 1
4 . 6 . . . 2 . .
5 2 7 4 . . . . .
. . . . 2 5 6 7 4

[set([1, 3]), 4, 5, 2, 8, set([1, 3]), 7, 9, 6]
[set([8, 2, 3]), set([3, 6, 7]), set([8, 3]), set([9, 3, 6]), set([9, 3, 5, 6, 7]), 4, 1, set([8, 2, 5]), set([8, 2, 5])]
[set([8, 1, 2]), set([1, 6, 7]), 9, set([1, 6]), set([5, 6, 7]), set([1, 6, 7]), 4, set([8, 2, 5]), 3]
[9, set([1, 3]), set([1, 2, 3, 4]), 7, set([3, 4]), set([8, 2, 3]), 5, 6, set([8, 2])]
[6, 8, set([2, 3]), 5, 1, set([2, 3]), 9, 4, 7]
[7, 5, set([2, 4]), set([8, 6]), set([4, 6]), 9, set([8, 3]), set([8, 2, 3]), 1]
[4, set([1, 3, 9]), 6, set([8, 1, 3, 9]), set([9, 3, 7]), set([8, 1, 3, 7]), 2, set([8, 1, 3, 5]), set([8, 9, 5])]
[5, 2, 7, 4, set([9, 3, 6]), set([8, 1, 3, 6]), set([8, 3]), set([8, 1, 3]), set([8, 9])]
[set([8, 1, 3]), set([1, 3, 9]), set([8, 1, 3]), set([1, 3, 9]), 2, 5, 6, 7, 4]



000530009
007000520
000082030
100000090
009723400
050000003
010940000
096000700
500071000

 SOLUTION
6 2 1 5 3 7 8 4 9
3 8 7 1 9 4 5 2 6
9 4 5 6 8 2 1 3 7
1 7 3 4 6 5 2 9 8
8 6 9 7 2 3 4 5 1
2 5 4 8 1 9 6 7 3
7 1 2 9 4 6 3 8 5
4 9 6 3 5 8 7 1 2
5 3 8 2 7 1 9 6 4
[6, 2, 1, 5, 3, 7, 8, 4, 9]
[3, 8, 7, 1, 9, 4, 5, 2, 6]
[9, 4, 5, 6, 8, 2, 1, 3, 7]
[1, 7, 3, 4, 6, 5, 2, 9, 8]
[8, 6, 9, 7, 2, 3, 4, 5, 1]
[2, 5, 4, 8, 1, 9, 6, 7, 3]
[7, 1, 2, 9, 4, 6, 3, 8, 5]
[4, 9, 6, 3, 5, 8, 7, 1, 2]
[5, 3, 8, 2, 7, 1, 9, 6, 4]



207060000
080000600
600300050
005010080
004507200
020030400
010008003
003000040
000070106


I SOLVED THIS ONE

000030016
900000500
006007090
004090005
500203004
200060700
010900200
007000001
340010000

SOLUTION
. . . . 3 9 . 1 6
9 . . . . . 5 . .
. . 6 . . 7 . 9 .
. . 4 . 9 . . 2 5
5 . . 2 . 3 . . 4
2 . . . 6 . 7 . .
. 1 . 9 . . 2 . .
. . 7 3 . . . . 1
3 4 . . 1 . . . .
[set([8, 4, 7]), set([8, 2, 5, 7]), set([8, 2, 5]), set([8, 4, 5]), 3, 9, set([8, 4]), 1, 6]
[9, set([8, 3]), set([8, 1, 3]), set([8, 1, 4, 6]), set([8, 2, 4]), set([8, 1, 2, 4, 6]), 5, set([8, 3, 4, 7]), set([8, 2, 3, 7])]
[set([8, 1, 4]), set([8, 3, 5]), 6, set([8, 1, 4, 5]), set([8, 2, 4, 5]), 7, set([8, 3, 4]), 9, set([8, 2, 3])]
[set([8, 1, 6, 7]), set([8, 3, 6, 7]), 4, set([8, 1, 7]), 9, set([8, 1]), set([8, 1, 3, 6]), 2, 5]
[5, set([8, 9, 6, 7]), set([8, 1, 9]), 2, set([8, 7]), 3, set([8, 1, 6, 9]), set([8, 6]), 4]
[2, set([8, 9, 3]), set([8, 1, 3, 9]), set([8, 1, 4, 5]), 6, set([8, 1, 4, 5]), 7, set([8, 3]), set([8, 9, 3])]
[set([8, 6]), 1, set([8, 5]), 9, set([8, 4, 5, 7]), set([8, 4, 5, 6]), 2, set([3, 4, 5, 6, 7, 8]), set([8, 3, 7])]
[set([8, 6]), set([8, 9, 2, 5, 6]), 7, 3, set([8, 2, 4, 5]), set([8, 2, 4, 5, 6]), set([8, 9, 4, 6]), set([8, 4, 5, 6]), 1]
[3, 4, set([8, 9, 2, 5]), set([8, 5, 6, 7]), 1, set([8, 2, 5, 6]), set([8, 9, 6]), set([8, 5, 6, 7]), set([8, 9, 7])]


 SOLUTION
. . . . 3 9 . 1 6
9 . . . . . 5 . .
. . 6 . . 7 . 9 .
. . 4 . 9 . . 2 5
5 . . 2 . 3 . . 4
2 . . . 6 . 7 . .
. 1 5 9 . . 2 . .
. . 7 3 . . . . 1
3 4 . . 1 . . . .
[set([4, 7]), set([8, 2, 5, 7]), set([8, 2]), set([8, 4, 5]), 3, 9, set([8, 4]), 1, 6]
[9, set([8, 3]), set([8, 1, 3]), set([8, 1, 4, 6]), set([8, 2, 4]), set([8, 1, 2, 4, 6]), 5, set([8, 3, 4, 7]), set([8, 2, 3, 7])]
[set([1, 4]), set([8, 3, 5]), 6, set([8, 1, 4, 5]), set([8, 2, 4, 5]), 7, set([8, 3, 4]), 9, set([8, 2, 3])]
[set([1, 7]), set([8, 3, 6, 7]), 4, set([8, 1, 7]), 9, set([8, 1]), set([8, 1, 3, 6]), 2, 5]
[5, set([8, 9, 6, 7]), set([8, 1, 9]), 2, set([8, 7]), 3, set([8, 1, 6, 9]), set([8, 6]), 4]
[2, set([8, 9, 3]), set([8, 1, 3, 9]), set([8, 1, 4, 5]), 6, set([8, 1, 4, 5]), 7, set([8, 3]), set([8, 9, 3])]
[set([8, 6]), 1, 5, 9, set([8, 4, 7]), set([8, 4, 6]), 2, set([8, 3, 4, 6, 7]), set([8, 3, 7])]
[set([8, 6]), set([9, 2]), 7, 3, set([8, 2, 4, 5]), set([8, 2, 4, 5, 6]), set([8, 9, 4, 6]), set([8, 4, 5, 6]), 1]
[3, 4, set([9, 2]), set([8, 5, 6, 7]), 1, set([8, 2, 5, 6]), set([8, 9, 6]), set([8, 5, 6, 7]), set([8, 9, 7])]
"""

"""
EASY

971000800
300800700
605000000
036701490
000302000
047906280
000000506
008005009
003000178
"""