# Prend en paramètre le chemin d'un fichier FQ. Si le fichier n'est pas de type FQ, le programme va redemander le chemin du fichier. La première séquence est le suffixe et le deuxième le préfixe
# Retoune l'alignement optimal suffixe-préfixe optimal, le score du chevauchement et le la longeur du chevauchement.
from Algo import *

def main():

    sequences = fileReader()

    #Contain dictionary [0], maximum value [1] and the coordinates of the max value [2]
    resultSP = suffixPrefixAlignment(sequences[0],sequences[1])
    
    alignment = optimalAlignment(sequences[0], sequences[1], resultSP[0], resultSP[2])

    alignmentPrefix = alignment[0][::-1]
    alignmentSuffix = alignment[1][::-1]

    print( sequences[0][0 : len(sequences[0])  - resultSP[2][1]] + alignmentSuffix)
    print( len(alignmentSuffix) * " " + alignmentPrefix + sequences[1][resultSP[2][1] : len(sequences[1])])
    print("Score = {}".format(resultSP[1]))
    print("longueur chevauchement = {}".format(len(alignmentPrefix)))
   

if __name__ == "__main__":
    main()
