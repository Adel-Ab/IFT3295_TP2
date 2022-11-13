
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
                if char != " " and char != "\n":
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
    gapPenalityOpen = -10
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
            
            # First row and column handling
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


def findCentralSequence(sequences, scoresInfo):
    maxScore = -math.inf
    indexMaxScore = 0
    matrixScore = []
    
    for i  in range (len(sequences)):
        matrixScore.append(0)
        for j in range(len(sequences)):

            if j != i:
                value = gapAlignment(sequences[i], sequences[j], scoresInfo)
                score = value[4]
                matrixScore[i] += score

    for i in range(len(matrixScore)):
        if matrixScore[i] > maxScore:
            maxScore = matrixScore[i]
            indexMaxScore = i

    return (indexMaxScore, maxScore)

def findMultipleAlignment(sequences, sequenceIndex, scoresInfo):
    centralSequence = sequences[sequenceIndex]
    alignSequences = []

    for i in range(len(sequences)):

        if i != sequenceIndex:
            result = gapAlignment(centralSequence, sequences[i], scoresInfo)
            position = (len(centralSequence), len(sequences[i]))
            alignment = optimalAlignment(centralSequence, sequences[i], result[0], result[1], result[2], position, result[3])

            j = 0
            while j < len(centralSequence):    
                if centralSequence[j] != alignment[0][j]:
                    centralSequence = centralSequence[:j] + "*" + centralSequence[j:]
                    for k in range (len(alignSequences)):
                        alignSequences[k] = alignSequences[k][:j] + "*" + alignSequences[k][j:]           
                j += 1

            alignSequences.append(alignment[1])

    alignSequences.insert(0, centralSequence)
    return alignSequences

            
            
    
def optimalAlignment(sequenceRow, sequenceColumn, matrixDictM, matrixDictX, matrixDictY, position, currentMatrix):
    optAlign = ()
    alignment = ("", "")
    if position[0] != 0 and position[1] != 0:
    
        if currentMatrix == "M":
            optAlign = optAlignM(matrixDictM, matrixDictX, matrixDictY, position, sequenceRow, sequenceColumn)
                
        if currentMatrix == "X":
            optAlign = optAlignX(matrixDictM, matrixDictX, position, sequenceRow)
                          
        if currentMatrix == "Y":
             optAlign = optAlignY(matrixDictM, matrixDictY, position, sequenceColumn)
            
                
        subAlignment =  optimalAlignment(sequenceRow, sequenceColumn, matrixDictM, matrixDictX, matrixDictY, optAlign[1], optAlign[2])
        alignment = optAlign[0]
        alignment = (subAlignment[0] + alignment[0], subAlignment[1] + alignment[1])

    return alignment


def optAlignM(matrixDictM, matrixDictX, matrixDictY, position, sequenceRow, sequenceColumn):
    maxValue = ""
    alignment = (sequenceRow[position[0] - 1], sequenceColumn[position[1] - 1])
    positionMaxValue = (position[0] - 1, position[1] - 1)
    newCurrentMatrix = ""


    if matrixDictM[position].M:
        maxValue = matrixDictM[positionMaxValue].score
        newCurrentMatrix = "M"

    if matrixDictM[position].X:
        if maxValue == "" or maxValue < matrixDictX[positionMaxValue].score:
            maxValue = matrixDictX[positionMaxValue].score
            newCurrentMatrix = "X"

    if matrixDictM[position].Y:
        if maxValue == "" or maxValue < matrixDictY[positionMaxValue].score:
            maxValue = matrixDictY[positionMaxValue].score
            newCurrentMatrix = "Y"

    return (alignment, positionMaxValue, newCurrentMatrix)


def optAlignX(matrixDictM, matrixDictX, position, sequenceRow):
    maxValue = ""
    alignment = (sequenceRow[position[0] - 1], "*")
    positionMaxValue = (position[0] - 1, position[1])
    newCurrentMatrix = ""


    if matrixDictX[position].M:
        maxValue = matrixDictM[positionMaxValue].score
        newCurrentMatrix = "M"

    if matrixDictX[position].X:
        if maxValue == "" or maxValue < matrixDictX[positionMaxValue].score:
            maxValue = matrixDictX[positionMaxValue].score
            newCurrentMatrix = "X"

    return (alignment, positionMaxValue, newCurrentMatrix)


def optAlignY(matrixDictM, matrixDictY, position, sequenceColumn):
    maxValue = ""
    alignment = ("*", sequenceColumn[position[1] - 1])
    positionMaxValue = (position[0], position[1] - 1)
    newCurrentMatrix = ""


    if matrixDictY[position].M:
        maxValue = matrixDictM[positionMaxValue].score
        newCurrentMatrix = "M"

    if matrixDictY[position].Y:
        if maxValue == "" or maxValue < matrixDictY[positionMaxValue].score:
            maxValue = matrixDictY[positionMaxValue].score
            newCurrentMatrix = "Y"

    return (alignment, positionMaxValue, newCurrentMatrix)
