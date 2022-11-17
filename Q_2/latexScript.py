
from Algo import *

# This function is the main one but formated to give latex lines
# ready to be pasted in overleaf to visualize the matrix
def LatexScript():

    scoresInfo = blosumFileReader()
    sequences = fileReader()
    matrixScore = []
    
    for i  in range(len(sequences) + 1):

        matrixScore.append([])
        for j in range(len(sequences) + 1):

           
            if i == 0 and j == 0:
                matrixScore[0].append(" & ")
                
            elif i == 0:
                matrixScore[i].append("S" + str(j) + " & ")
            
            elif j == 0:
                 matrixScore[i].append("S" + str(i) + " & ")

            elif j == i:
                matrixScore[i].append(" x & ")

            else:
                value = gapAlignment(sequences[i -1], sequences[j - 1], scoresInfo)
                score = value[4]
                matrixScore[i].append(str(score) + " & ")


    for i  in range(len(sequences) + 1):
        test = "".join(matrixScore[i])
        print("\hline")
        print(test)


def latexScriptConsensus(arrayConsensus):
    matrixConsensus = []
    
    for i in range(2):
        matrixConsensus.append([])
        for j in range(len(arrayConsensus)):
        
            if i == 0:
                matrixConsensus[i].append("C" + str(j+1) + " & ")

            else:
                matrixConsensus[i].append(arrayConsensus[j] + " & ")


    start = 0
    finish = 18
    for j in range (len(arrayConsensus) // 18): 
        for i in range(len(matrixConsensus)):
            if(finish < len(arrayConsensus)):
                test = "".join(matrixConsensus[i][start:finish])
            else:
                test = "".join(matrixConsensus[i][start:])
            print("\hline")
            print(test)
        start += 18
        finish += 18
