
from Cell import *

# Ask the user to input the sequence
def getSequence():

    while True:

        verificator = True
        print("Veuillez entrer la séquence à replier")
        sequence = input()

        # Verifying if the input is a correct sequence
        for char in sequence:
    
            if char not in ['A','U','C','G'] :
                print(" ERREUR: La séquence fournie contient un élément qui n'est pas un nucléotide. ")
                verificator = False

        if verificator:
            return sequence

# Reverse and complement a sequence by replacing each nucleotide by it's complementary one
def inverseComplement(sequence):
    # Reverse the sequence
    reversed = sequence[::-1]
    # Replace A by U and U by A
    reversedComplementedAU = reversed.replace('A','T').replace('U','A').replace('T','U')
    # Replace G by C and C by G
    reversedComplementedAUGC = reversedComplementedAU.replace('G','T').replace('C','G').replace('T','C')

    return(reversedComplementedAUGC)


# Apply a simple version of the Nussinov Algorithm to a sequence and its reversed and complemented 
# version to create a matrix from wich we can output the optimal folding combination 

def simpleNussinov(sequenceRow, sequenceColumn):

    # Hard coded scoring values
    match = 1
    mismatch = 0
    # Highest cell score to date
    maxScore = 0
    maxScorePosition = (0,0)
    # Dict with key : values = index tuple i,j : Cell object
    matrixDict = {}
    
    # Go through matrix columns
    for j in range(len(sequenceColumn)):
        
        # Keeping count of the two first cells as anti-diagonal cells
        diagsCount = 2

        # Go through matrix rows from last to first
        for i in range(len(sequenceRow)-2-j,len(sequenceRow)):
        
            # Create the 0 anti diagonal for the first two cells
            # Note: Last column case; Cell at i =-1 and i=0 will be created as a diag cell 
            if (diagsCount != 0):
                diagsCount -= 1
                matrixDict[(i,j)] = Cell(0,0,0,True)

            # If not an anti diagonal cell
            else:
                # Get the score of the previous row cell
                valueFromRow =  matrixDict[(i-1,j)].score
                # Get the score of the previous column cell
                valueFromColumn = matrixDict[(i,j-1)].score
                # Calculate if there is a match or not
                matching = match if(sequenceColumn[j]==sequenceRow[i]) else mismatch
                # Get the score of the diagonale value summed with the matching\mismatch value
                valueFromDiag = matrixDict[(i-1,j-1)].score + matching
                # Create cell
                matrixDict[(i,j)] = Cell(valueFromRow, valueFromColumn, valueFromDiag)

                # Update the highest score and its position
                if maxScore < max(valueFromRow, valueFromColumn, valueFromDiag):
                    maxScore = max(valueFromRow, valueFromColumn, valueFromDiag)
                    maxScorePosition = (i,j)
                    
            #### TESTING PRINT ###
            print(matrixDict[(i,j)].score)
                    
    return (matrixDict, maxScore, maxScorePosition)




######## backtracking TO DO 

def optimalAlignment(sequenceSuffix, sequencePrefix, cellDictionary, position):

    # prefix first, suffix second
    alignment = ("","")
    maxValue = ""
    positionMaxValue = (0,0)


    if position[0] != 0:
    
        if cellDictionary[position].diag:
                maxValue = cellDictionary[(position[0] - 1,position[1] - 1)].score
                positionMaxValue = (position[0] - 1,position[1] - 1)
                alignment = (alignment[0] + sequencePrefix[position[1] - 1],alignment[1] + sequenceSuffix[position[0] - 1])

        if cellDictionary[position].up:
            if maxValue == "" or maxValue < cellDictionary[(position[0] - 1,position[1])].score:
                maxValue = cellDictionary[(position[0]-1,position[1])].score
                positionMaxValue = (position[0] - 1,position[1])
                alignment = (alignment[0] + "_" ,alignment[1] + sequenceSuffix[position[0] - 1])
                        
                
        if cellDictionary[position].left:
            if maxValue == "" or maxValue < cellDictionary[(position[0],position[1] - 1)].score:
                maxValue = cellDictionary[(position[0],position[1] - 1)].score
                positionMaxValue = (position[0],position[1]- 1)
                alignment = (alignment[0] + sequencePrefix[position[1] - 1] ,alignment[1] + "_")
                
        subAlignment =  optimalAlignment(sequenceSuffix, sequencePrefix, cellDictionary, positionMaxValue)
        alignment = (alignment[0] + subAlignment[0], alignment[1] + subAlignment[1])

    return alignment
        