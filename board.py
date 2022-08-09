import pandas as pd

#bit space
class Space(object):
    '''
    Class that stores a space as integer

    If the user gives a string, it should be in algebraic notation

    If the user gives an integer, all leading zeroes are assumed
    '''
    def __init__(self, input_value):
        if isinstance(input_value, str):
            #for algebraic notation file
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            assert ((input_value[0:1] in letters and 1 <= int(input_value[1:2]) <= 8), 
                "Not valid algebraic notation.")
            
            #converting to integer
            row = int(input_value[1:2]) - 1
            file = letters.index(input_value[0:1])
            self.value = 16*row + file

        elif isinstance(input_value, int):
            
            """ assert ((0 <= input_value < 128), "Value row is out of range.")
            assert ((0 <= input_value % 16 < 8), "Value file (column) is off the board.") """
            self.value = input_value #allow for invalid spaces for isValid method
    
    def isValid(self):
        return (0 <= self.value < 128) and (0 <= (self.value % 16) < 8)
    
    #for converting space to board representation
    def getIndices(self):
        file = self.value % 16
        row = self.value // 16 #for white view
        return row, file

class Team(object):
    '''
    Class that stores a team's pieces

    Enter true for black_team, false for white_team
    '''
    def __init__(self, black_team):
        self.pawns = [i for i in range(16 + 80*black_team, 24 + 80*black_team)]
        self.rooks = [0 + 112*black_team, 7 + 112*black_team]
        self.knights = [1 + 112*black_team, 6 + 112*black_team]
        self.bishops = [2 + 112*black_team, 5 + 112*black_team]
        self.royals = [4 + 112*black_team, 3 + 112*black_team]

class Chess:
    '''
    Class for Computer Chess
    '''
    def __init__(self):
        self.white = Team(black_team = False)
        self.black = Team(black_team = True)
        self.white_move = True

    #returns board as pandas df, for now rotate is off
    def display(self, rotate = None):
        blanks = [[0] * 8] * 8
        board = pd.DataFrame(blanks)
        names = ["white pawn"] * 8 + ["white rook"] * 2 + ["white knight"] * 2 + ["white bishop"] * 2 + ["white queen"] + ["white king"] + ["black pawn"] * 8 + ["black rook"] * 2 + ["black knight"] * 2 + ["black bishop"] * 2 + ["black queen"] + ["black king"]

        for i in range(0, 32): #white pawns
            row, file = Space(self.array[i]).getIndices()
            board.loc[row, file] = names[i]

        board.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        board.index = [1+i for i in range(0, 8)]
        board.sort_index(inplace=True, ascending=False)
        return board

    def _findPawn_(self, text):
        row, file = Space(text).getIndices()
        closest = None
        index = 16 - self.white_move * 16
        found = False

        while(not found and index < (32 - self.white_move * 16)):
            if (self.board.array[index] % 16) == file:
                distance = self.board.array[index] // 16 - row
                if self.white_move: #whether pawn should be infront or behind destination space
                    distance *= -1

                if distance == 1:
                    closest = index
                    found = True
                elif distance == 2 and ((row == 3 and self.white_move) or (row == 4 and not self.white_move)):
                    closest = index
            index += 1
        
        assert closest is not None, "Not a valid move."
        return closest

    def move(self, text):
        counter = 16 - True * 16 #for black pieces

        if len(text) == 2: #pawn moving forward
            destination = text
            closest = self._findPawn_(text)
            assert Space(text).value
        
        if text[0:1].lower() == 'r': #rook moving
            return None
        
        self.board.array[closest] = Space(destination).value #moving piece
        self.white_move = not self.white_move #switching turn