#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
from statistics import stdev

ROW = "ABCDEFGHI"
COL = "123456789"

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def print_subgrid(board):
    """Helper function to print board in a square."""
    print("-----------------")
    R = "ABC"
    C = "123"
    for i in R:
        row = ''
        for j in C:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def subgrids(board):
    # determine the subgrids in the board
    # print_board(board)
    subgrids_all = []
    subgrid1_keys = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
    subgrid1 = {key: value for key, value in board.items() if key in subgrid1_keys}
    subgrid2_keys = ["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"]
    subgrid2 = {key: value for key, value in board.items() if key in subgrid2_keys}
    subgrid3_keys = ["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"]
    subgrid3 = {key: value for key, value in board.items() if key in subgrid3_keys}

    subgrid4_keys = ["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"]
    subgrid4 = {key: value for key, value in board.items() if key in subgrid4_keys}
    subgrid5_keys = ["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"]
    subgrid5 = {key: value for key, value in board.items() if key in subgrid5_keys}
    subgrid6_keys = ["D7", "D8", "D9", "E7", "E8", "E9", "F7", "F8", "F9"]
    subgrid6 = {key: value for key, value in board.items() if key in subgrid6_keys}

    subgrid7_keys = ["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"]
    subgrid7 = {key: value for key, value in board.items() if key in subgrid7_keys}
    subgrid8_keys = ["G4", "G5", "G6", "H4", "H5", "H6", "I4", "I5", "I6"]
    subgrid8 = {key: value for key, value in board.items() if key in subgrid8_keys}
    subgrid9_keys = ["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"]
    subgrid9 = {key: value for key, value in board.items() if key in subgrid9_keys}
    subgrids_all.extend([subgrid1, subgrid2, subgrid3, subgrid4, subgrid5, subgrid6, subgrid7, subgrid8,
                         subgrid9])  # list of dictionaries
    return subgrids_all

def min_remaining_values(empty_tiles, board):
    # determine the subgrids in the board
    subgrids_all = subgrids(board)

    # determine the MRV for the empty tiles
    empty_tiles_MRV = {}
    min = 9
    t = None #tile with the least legal domain values
    for tile in empty_tiles:

        # check in which subgrid it's in
        subgrid_values = []
        for subgrid in subgrids_all:
            if tile in list(subgrid.keys()):
                for key in subgrid.keys():
                    if subgrid[key]:  # has assigned value
                        subgrid_values.append(subgrid[key])
            else:
                continue

        # determine which row and column to check
        tile_row = tile[0] #Letters A,B,C ..
        tile_col = tile[1] #Numbers 1,2,3, ...

        # check column assigned values
        row_values = []
        for r in ROW:
            var = r + tile_col
            if board[var]:  # has assigned value
                row_values.append(board[var])

        # check row assigned values
        col_values = []
        for c in COL:
            var = tile_row + c
            if board[var]:  # has assigned value
                col_values.append(board[var])

        # Set of values the tile can't take
        taken_values = set().union(row_values, col_values, subgrid_values)

        # create a set of MRV for the empty tile
        mrv = set()
        for i in range(1,10):
            if i not in taken_values:
                mrv.add(i)

        mrv = sorted(mrv)

        empty_tiles_MRV[tile] = mrv
        if len(mrv) < min:
            min = len(mrv)
            t = tile

    return t, empty_tiles_MRV #returns subgrid, tile with least domain, dictionary of empty tiles and their MRVs set

def findEmpty(board):
    # determine where the empty tiles are in the board
    empty_tiles = []
    for variable, value in board.items():
        if value == 0:
            empty_tiles.append(variable)
    return empty_tiles

def FC(value, empty_tiles_MRV, tile, subgrid):
    #check if assigning this current value to tile is safe
    #with respect to values in the row, column, and subgrid
    tile_row = tile[0]
    tile_column = tile[1]

    for r in ROW:
        if r != tile_row:
            var = r + tile_column
            if var in empty_tiles_MRV:
                mrv = empty_tiles_MRV[var]
                #determine if current value is the only value in the domain
                if len(mrv) == 1 and value in mrv:
                    return False

    for c in COL:
        if c != tile_column:
            var = tile_row + c
            if var in empty_tiles_MRV:
                mrv = empty_tiles_MRV[tile_row + c]
                # determine if current value is the only value in the domain
                if len(mrv) == 1 and value in mrv:
                    return False

    subgrid_values = []
    for key in subgrid.keys(): #key is the variable
        subgrid_values.append(board[key])

    #check if value violates constraint in subgrid
    if value in subgrid_values:
        return False

    return True

def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this

    empty_tiles = findEmpty(board)

    # check if board is solved
    if len(empty_tiles) == 0:
        #board solved
        solved_board = board
        return True

    #determine the MRV for the empty tiles
    tile, empty_tiles_MRV = min_remaining_values(empty_tiles, board)

    sg = None
    for subgrid in subgrids(board):
        if tile in list(subgrid.keys()):
            sg = subgrid
            break


    #find the tile with the least legal domain values and order them as such
    domain = list(empty_tiles_MRV[tile])

    for value in domain:
        #apply forward checking
        result = FC(value, empty_tiles_MRV, tile, sg)
        if result:
            #value is safe to assign
            board[tile] = value
            #perform backtracking
            if backtracking(board):
                #no more empty tiles/all variables are assigned
                solved_board = board
                return solved_board
            else:
                board[tile] = 0


    return False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        #Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        i = 0
        total_runtime = 0
        list_runtime = []
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print("printing board ----------------")
            print_board(board)

            # Solve with backtracking
            start = time.time()
            solved_board = backtracking(board)
            end = time.time()
            runtime = round(end - start, 8)
            total_runtime += runtime
            list_runtime.append(runtime)
            if solved_board:
                i += 1

            # Print solved board. TODO: Comment this out when timing runs.
            print("printing solved board ----------------")
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        # print("Finishing all boards in file.")
        # print("number of boards solved:", i)
        # print("min time: ", min(list_runtime))
        # print("max time: ", max(list_runtime))
        # print("mean of runtime: ", total_runtime/400)
        # print("stdv time: ", stdev(list_runtime))