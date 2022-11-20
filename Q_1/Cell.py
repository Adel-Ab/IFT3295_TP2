

class Cell:

    def __init__(self, valueFromRow, valueFromColumn, valueFromDiagonal, matching, diagLimit = False):
        
        # Setting the arrows activation at false
        self.up = False
        self.left = False
        self.diag = False

        # Matching situation of the cell i,j
        self.match = matching
        # If the cell is part of the anti-diagonal limit
        self.diagLimit = diagLimit
        # Setting score at 0
        self.score = 0
           
        # If cell is not on the anti-diagonal
        if(not diagLimit):

            self.score = max(valueFromRow, valueFromColumn, valueFromDiagonal)

            # active the arrows by looking at the max score contributor(s)
            if self.score == valueFromRow:
                self.up = True
            if self.score == valueFromColumn:
                self.left = True
            if self.score == valueFromDiagonal:
                self.diag = True