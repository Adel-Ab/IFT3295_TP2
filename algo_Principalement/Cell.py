

class Cell:

    def __init__(self, valueFromRow, valueFromColumn, valueFromDiagonal, typeCell = -1):

        # Setting the arrows activation at false
        self.up = False
        self.left = False
        self.diag = False
        self.score = 0

        # If cell is on last column
         
        # If cell is on first row
        if typeCell == 1:
            self.score = valueFromRow

            # if last cell; no arrows
            if valueFromRow != 0:
                self.left = True
           
        # If cell is anywhere else
        else :
            self.score = max(valueFromRow, valueFromColumn, valueFromDiagonal)

            # active the arrows by looking at the max score contributor(s)
            if self.score == valueFromRow:
                self.up = True
            if self.score == valueFromColumn:
                self.left = True
            if self.score == valueFromDiagonal:
                self.diag = True