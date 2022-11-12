import math

class Cell:

    def __init__(self, valueFromM, valueFromX, valueFromY, matrixCell, typeCell = 1 ):

        # Setting the arrows activation at false
        self.M = False
        self.X = False
        self.Y = False
        self.matrixCell = matrixCell

        if typeCell == 0:
            self.score = valueFromM

        else:

            self.score = max(valueFromM, valueFromX, valueFromY)

            # active the arrows by looking at the max score contributor(s)

            if self.score == valueFromM:
                self.M = True
            if self.score == valueFromX:
                self.X = True
            if self.score == valueFromY:
                self.Y = True