# Prend en paramètre le chemin d'un fichier FQ. Si le fichier n'est pas de type FQ, le programme va redemander le chemin du fichier. La première séquence est le suffixe et le deuxième le préfixe
# Retoune l'alignement optimal suffixe-préfixe optimal, le score du chevauchement et le la longeur du chevauchement.
from Algo import *

def main():

    sequence = getSequence()
    sequenceInversedComplemented = inverseComplement(sequence)

    repliement = simpleNussinov(sequence,sequenceInversedComplemented)
    backTracking( sequence,((inverseComplement(sequence))[::-1]), repliement[0], (len(sequence)-1,len(sequence)-1))


    #### TO DO :
    # BACKTRACK
    # Clean up le max score,max position ?
    
   

if __name__ == "__main__":
    main()
