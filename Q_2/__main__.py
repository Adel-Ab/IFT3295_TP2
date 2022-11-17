# Prend en paramètre le chemin d'un fichier FQ. Si le fichier n'est pas de type FQ, le programme va redemander le chemin du fichier. La première séquence est le suffixe et le deuxième le préfixe
# Retoune l'alignement optimal suffixe-préfixe optimal, le score du chevauchement et le la longeur du chevauchement.
from Algo import *
from latexScript import *

def main():

    scoresInfo = blosumFileReader()
    sequences = fileReader()

    resultCentralSequence = findCentralSequence(sequences, scoresInfo)
    print("Score séquence centrale : " + str(resultCentralSequence[1]))

    print("Séquence centrale : " + str(resultCentralSequence[0] + 1))

    alignment = findMultipleAlignment(sequences, resultCentralSequence[0], scoresInfo)

    print("Score SP :" + str(SPScore(alignment)))

    for i in alignment:
        print(i)

    arrayConsensus = consensusPerColumn(alignment)

    #latexScriptConsensus(arrayConsensus)
     
   
if __name__ == "__main__":
    main()
