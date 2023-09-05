import numpy as np
import os
def ajouter_ligne_colonne(mat):
    nb_lignes = len(mat)
    nb_colonnes = len(mat[0])
    matpro = [[0] * (nb_colonnes+2)]  # Ajoute une ligne de zéros en haut
    for i in range(nb_lignes):
        matpro.append([0] + mat[i] + [0])  # Ajoute une colonne de zéros à gauche et à droite
    matpro.append([0] * (nb_colonnes+2))  # Ajoute une ligne de zéros en bas
    return matpro


def parcourir_matrice(mat):
    nb_lignes = len(mat)
    nb_colonnes = len(mat[0])
    n=[]
    f=[]
    matrice = [[0, 0], [0, 0]]
    for i in range(nb_colonnes-1):
        if i !=nb_colonnes-1:
            for j in range(nb_lignes-1):
                if j!=nb_lignes-1:
                    b=j
                    
                    for o in range(2):
                        c=i
                        for p in range(2):
                            matrice[o][p] =mat[b][c]
                            c=c+1
                        b=b+1
                        
                    k=np.sum(matrice)
                    n.append(k)
                    
                    if k==2:
                        diagonale = [matrice[i][i] for i in range(2)]
                        diagonaleinv=[matrice[0][1],matrice[1][0]]
                        if diagonale == [1, 1]:
                            f.append(1)  
                        elif diagonaleinv==[1, 1]:
                            f.append(1)  
                        else:
                            f.append(0)
                    else:
                        f.append(0)
                                           
                else:
                    break
        else:
            break
    return n,f


def resultat(n,f):
    _3entr=0
    _4entr=0
    _5entr=0
    for i in range(len(n)):
        if n[i]==1:
            _3entr=_3entr+1
        if n[i]==2:
            if f[i]==1:
                _5entr=_5entr+1
            else:
                _4entr=_4entr+1
        if n[i]==3:
            _5entr=_5entr+1
        if n[i]==4:
            _5entr=_5entr+1
    # print("Vous avez besoin de :\n"+"2 entree :"+str(_3entr) + "\n"+"3 entree :"+str(_4entr)+"\n"+"4 entree :"+str(_5entr)+"\n")
    return _3entr,_4entr,_5entr
        
def detection_de_bord(mat):
    matpro=ajouter_ligne_colonne(mat)
    n,f=parcourir_matrice(matpro)
    _3entr,_4entr,_5entr=resultat(n,f) 
    # print(f)
    # print(n)
   
    return _3entr,_4entr,_5entr
