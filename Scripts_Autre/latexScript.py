
from Algo import *

# This function is the main one but formated to give latex lines
# ready to be pasted in overleaf to visualize the matrix
def LatexScript():

    sequences = fileReader()

    matrixScore = []
    

    for i  in range(len(sequences) + 1):

        matrixScore.append([])
        for j in range(len(sequences) + 1):

           
            if i == 0 and j == 0:
                matrixScore[0].append(" & ")
                
            elif i == 0:
                matrixScore[i].append(str(j) + " & ")
            
            elif j == 0:
                 matrixScore[i].append(str(i) + " & ")

            elif j == i:
                matrixScore[i].append(" x & ")

            else:
                value = suffixPrefixAlignment(sequences[i -1], sequences[j - 1])
                score = value[1]
                matrixScore[i].append(str(score) + " & ")


    for i  in range(len(sequences) + 1):
        test = "".join(matrixScore[i])
        print("\hline")
        print(test)