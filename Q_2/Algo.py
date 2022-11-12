
from Cell import *
import math

# Ask the user to input path of .fq file
def GetPathBlosum():
    isLooping = True
    path = ""

    while isLooping:
        print("Entrer le path du ficher blosom")
        path = input()

        if ".txt" in path: 
            isLooping = False
        else:
            print("Pas le bon type de fichier. Réessayer")

    return path

# Reads file to find and return the sequences
def blosumFileReader():
    scores = []
    i = 0
    isFirstLign = True
    letterDic = {}

    file = open(GetPathBlosum(), 'r+')

    for line in file:

        if isFirstLign:   
            compteur = 0
            for char in line:
                if char.isalpha():
                    letterDic[char] = compteur
                    compteur += 1
            isFirstLign = False

        else:
            compteur = 1
            scores.append([])
            while compteur < len(line):
               
                if line[compteur] == "-":
                    scores[i].append(int(line[compteur : compteur + 2]))
                    compteur += 1

                elif line[compteur].isnumeric():
                    scores[i].append(int(line[compteur]))

                compteur += 1
                   
            i += 1

    return (scores, letterDic)


def GetPath():
    isLooping = True
    path = ""

    while isLooping:
        print("Entrer le path du ficher")
        path = input()

        if ".fasta" in path: 
            isLooping = False
        else:
            print("Pas le bon type de fichier. Réessayer")

    return path

# Reads file to find and return the sequences
def fileReader():
    sequences = []
    file = open(GetPath(), 'r+')
    currentSequence = ""

    for line in file:
        if ">" in line and currentSequence != "":   
            sequences.append(currentSequence.strip().replace("\n",""))
            currentSequence = ""
        
        elif  ">" not in line:
            currentSequence += line

    sequences.append(currentSequence.strip().replace("\n",""))
    return sequences


# Calculate and return the cell score matrix through a dictionary
# along with the max score and max score position in the matrix
def gapAlignment(sequenceRow, sequenceColumn, scoresInfo):

    # Hard coded scoring values
    # TO REPLACE IN CODE
    gapPenalityOpen = -3
    gapPenalityExt = -1

    # Highest cell score to date
    maxScoreMatrix = ""
    
    # Dict with key : values = index tuple i,j : Cell object
    matrixDictM = {}
    matrixDictX = {}
    matrixDictY = {}

    # Go through matrix rows
    for i in range(len(sequenceRow)+1):

        for j in range((len(sequenceColumn))+1):
            
            # First row handling
            if i==0 and j==0: 
                matrixDictM[(i,j)] = Cell(0, 0, 0, "M", 0)
                matrixDictX[(i,j)] = Cell(gapPenalityOpen, gapPenalityOpen, gapPenalityOpen, "X", 0)
                matrixDictY[(i,j)] = Cell(gapPenalityOpen, gapPenalityOpen, gapPenalityOpen, "Y", 0)
    
                 
            # Other cells handling
            else:
                aligmentM(matrixDictM, matrixDictX, matrixDictY, scoresInfo, i, j, sequenceRow, sequenceColumn)
                aligmentX(matrixDictM, matrixDictX, gapPenalityOpen, gapPenalityExt, i, j)
                aligmentY(matrixDictM, matrixDictY, gapPenalityOpen, gapPenalityExt, i, j)

    maxScore = max(matrixDictM[(len(sequenceRow),len(sequenceColumn))].score, matrixDictX[(len(sequenceRow),len(sequenceColumn))].score, matrixDictY[(len(sequenceRow),len(sequenceColumn))].score)

    if maxScore == matrixDictY[(len(sequenceRow),len(sequenceColumn))].score:
        maxScoreMatrix = "Y"

    elif maxScore == matrixDictX[(len(sequenceRow),len(sequenceColumn))].score:
         maxScoreMatrix = "X"

    elif maxScore == matrixDictM[(len(sequenceRow),len(sequenceColumn))].score:
         maxScoreMatrix = "M"
                  
    return (matrixDictM, matrixDictX, matrixDictY, maxScoreMatrix, maxScore)


def aligmentM(matrixDictM, matrixDictX, matrixDictY, scoresInfo, i, j, sequenceRow, sequenceColumn):
    if i-1 < 0 or j-1 < 0:
         matrixDictM[(i,j)] = Cell(-math.inf, -math.inf, -math.inf, "M", 0)

    else:
        scores = scoresInfo[0]
        letterDictionnary = scoresInfo[1]

        valueM = matrixDictM[(i-1,j-1)].score + scores[letterDictionnary[sequenceRow[i-1]]] [letterDictionnary[sequenceColumn[j-1]]]
        valueX = matrixDictX[(i-1,j-1)].score + scores[letterDictionnary[sequenceRow[i-1]]] [letterDictionnary[sequenceColumn[j-1]]]
        valueY = matrixDictY[(i-1,j-1)].score + scores[letterDictionnary[sequenceRow[i-1]]] [letterDictionnary[sequenceColumn[j-1]]]

        matrixDictM[(i,j)] = Cell(valueM, valueX, valueY, "M")


def aligmentX(matrixDictM, matrixDictX, gapPenalityOpen, gapPenalityExt, i, j):
    if i-1 < 0 :
         matrixDictX[(i,j)] = Cell(-math.inf, -math.inf, -math.inf, "X", 0)

    else:
        valueX = matrixDictX[(i-1,j)].score + gapPenalityExt
        valueM = matrixDictM[(i-1,j)].score + gapPenalityOpen + gapPenalityExt
        matrixDictX[(i,j)] = Cell(valueM, valueX, -math.inf, "X")


def aligmentY(matrixDictM, matrixDictY, gapPenalityOpen, gapPenalityExt, i, j):
    if j-1 < 0:
        matrixDictY[(i,j)] = Cell(-math.inf, -math.inf, -math.inf, "Y", 0)
    else:    
        valueY = matrixDictY[(i,j-1)].score + gapPenalityExt
        valueM = matrixDictM[(i,j-1)].score + gapPenalityOpen + gapPenalityExt
        matrixDictY[(i,j)] = Cell(valueM, -math.inf, valueY, "Y")

    



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
        