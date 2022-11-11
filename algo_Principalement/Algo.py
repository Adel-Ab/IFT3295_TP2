
from Cell import *

# Ask the user to input path of .fq file
def GetPath():
    isLooping = True
    path = ""

    while isLooping:
        print("Entrer le path du ficher")
        path = input()

        if ".fq" in path: 
            isLooping = False
        else:
            print("Pas le bon type de fichier. Réessayer")

    return path

# Reads file to find and return the sequences
def fileReader():
    sequences = []
    file = open(GetPath(), 'r+')

    for line in file:
        if "@" in line:   
            sequence = next(file).replace("\n","")
            sequences.append(sequence)
    return sequences

# Calculate and return the cell score matrix through a dictionary
# along with the max score and max score position in the matrix
def suffixPrefixAlignment(sequenceRow, sequenceColumn):

    # Hard coded scoring values
    # TO REPLACE IN CODE
    match = 4
    mismatch = -4
    indel = -8
    # Highest cell score to date
    maxScore = 0
    maxScorePosition = (0,0)

    
    # Dict with key : values = index tuple i,j : Cell object
    matrixDict = {}
    
    # Go through matrix rows
    for i in range(len(sequenceRow)+1):

        # Go through matrix columns from last to first
        for j in range((len(sequenceColumn)) + 1,):
            
            # First row handling
            if i==0:
                # Create cell in dict; see Cell Class __init__ with typeCell == 1 
                matrixDict[(i,j)] = Cell(j *(indel),0,0,1)
            
            # Last column handling
            elif j==0:
                # Create cell in dict; see Cell Class __init__ with typeCell == 0
                matrixDict[(i,j)] = Cell(0,0,0,0)
            
            # Other cells handling
            else:
                # Calculate the previous cell
                valueFromColumn = matrixDict[(i,j-1)].score + indel
                valueFromRow =  matrixDict[(i-1,j)].score + indel
                valueFromDiagonal = 0
                
                # If match
                if sequenceRow[i-1] == sequenceColumn[j-1]:
                    # Add 4 to the previous diag cell
                    valueFromDiagonal = matrixDict[(i-1,j-1)].score + match
 
                # If no match
                else:
                    # Remove 4 points to the previous diag cell
                    valueFromDiagonal = matrixDict[(i-1,j-1)].score + mismatch
    
                matrixDict[(i,j)] = Cell(valueFromRow, valueFromColumn, valueFromDiagonal)
                   
                # Update the highest score and its position
                if i == len(sequenceRow) and maxScore < max(valueFromRow, valueFromColumn, valueFromDiagonal):
                    maxScore = max(valueFromRow, valueFromColumn, valueFromDiagonal)
                    maxScorePosition = (i,j)
                    
    return (matrixDict, maxScore, maxScorePosition)


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
        