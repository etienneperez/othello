import profile
import ssl
import numpy as np
from math import *
from tkinter import *
import tkinter as tk
from random import randint, random
import copy as copy
p_prof = 2
class Othellier(object):

    def __init__(self, prof,joueur,tablier):#,score = 0 ):
        self.prof = prof
        self.joueur = joueur
        self.tablier = tablier # matrice 8x8 contenant les Cases
        self.liste_coord_successeurs = []
        self.liste_successeurs = [] # liste des noms des successeurs
        #self.score = score # valeur de la fonction d'évaluation ou max/min des successeurs
        self.successeurs_bis()
        # self.joueur = joueur # "blanc" si c'est au joueur blanc de jouer, "noir" sinon   

    def successeurs_bis(self): 
        if self.prof > 0 : 
            for l in range(8):
                for c in range(8):
                    if self.tablier[l,c] == 0 : 
                        tablier_local = np.array([[0 for i in range (8)] for j in range (8)])
                        for lbis in range(8):
                            for cbis in range(8):
                                tablier_local[lbis,cbis] = self.tablier[lbis,cbis]
                            tablier_local[l,c] = self.joueur
                            isAccessible = False
                            isAccessibleB = False
                            isAccessibleBD = False
                            isAccessibleBG = False
                            isAccessibleG = False
                            isAccessibleD = False
                            isAccessibleH = False
                            isAccessibleHD = False
                            isAccessibleHG = False

                            #On regarde dans chaque direction : 
                            #BAS
                        pas_b = 1
                        while pas_b + l < 7 and tablier_local[l+pas_b,c] == -self.joueur : 
                            pas_b += 1
                        if (pas_b > 1) and (tablier_local[l+pas_b,c]== self.joueur) : 
                            isAccessible = True
                            isAccessibleB = True
                    
                            #HAUT
                        pas_h = 1
                        while l - pas_h > 0 and tablier_local[l-pas_h,c] == -self.joueur : 
                            pas_h += 1
                        if (pas_h > 1) and (tablier_local[l-pas_h,c]== self.joueur) : 
                            isAccessible = True
                            isAccessibleH = True   

                            #GAUCHE
                        pas_g = 1
                        while c - pas_g > 0 and tablier_local[l,c-pas_g] == -self.joueur : 
                            pas_g += 1
                        if (pas_g > 1) and (tablier_local[l,c-pas_g]== self.joueur) : 
                            isAccessible = True
                            isAccessibleG = True   

                            #DROITE
                        pas_d = 1
                        while c + pas_d < 7 and tablier_local[l,c+pas_d] == -self.joueur : 
                            pas_d += 1
                        if (pas_d > 1) and (tablier_local[l,c+pas_d]== self.joueur) : 
                            isAccessible = True
                            isAccessibleD = True
                                                                                 
                            #BAS-Gauche
                        pas_bg = 1
                        while pas_bg + l < 7 and c - pas_bg > 0 and tablier_local[l+pas_bg,c-pas_bg] == -self.joueur  : 
                            pas_bg += 1
                        if (pas_bg > 1) and (tablier_local[l+pas_bg,c-pas_bg]== self.joueur) : 
                            isAccessible = True
                            isAccessibleBG = True
                            
                            #Haut-Droite
                        pas_hd = 1
                        while l - pas_hd > 0 and c + pas_hd < 7 and tablier_local[l-pas_hd,c+pas_hd] == -self.joueur : 
                            pas_hd += 1
                        if (pas_hd > 1) and (tablier_local[l-pas_hd,c+pas_hd]== self.joueur) : 
                            isAccessible = True
                            isAccessibleHD = True  

                            #GAUCHE-Haut
                        pas_hg = 1
                        while c - pas_hg > 0 and l - pas_hg > 0  and tablier_local[l-pas_hg,c-pas_hg] == -self.joueur : 
                            pas_hg += 1
                        if (pas_hg > 1) and (tablier_local[l-pas_hg,c-pas_hg]== self.joueur) : 
                            isAccessible = True
                            isAccessibleHG = True
                             
                            #DROITE-Bas
                        pas_bd = 1
                        while c + pas_bd < 7 and pas_bd + l < 7 and tablier_local[l+pas_bd,c+pas_bd] == -self.joueur : 
                            pas_bd += 1
                        if (pas_bd > 1) and (tablier_local[l+pas_bd,c+pas_bd]== self.joueur) : 
                            isAccessible = True
                            isAccessibleBD = True
                            
                        if isAccessibleB :
                            for k in range(1,pas_b):                        
                                tablier_local[l+k,c] = self.joueur
                        if isAccessibleBD :
                            for k in range(1,pas_bd):
                                tablier_local[l+k,c+k] = self.joueur 
                        if isAccessibleBG :
                            for k in range(1,pas_bg):
                                tablier_local[l+k,c-k] = self.joueur
                        if isAccessibleG :
                            for k in range(1,pas_g):
                                tablier_local[l,c-k] = self.joueur 
                        if isAccessibleD :
                            for k in range(1,pas_d):
                                tablier_local[l,c+k] = self.joueur
                        if isAccessibleH :
                            for k in range(1,pas_h):
                                tablier_local[l-k,c] = self.joueur
                        if isAccessibleHD :
                            for k in range(1,pas_hd):
                                tablier_local[l-k,c+k] = self.joueur 
                        if isAccessibleHG :
                            for k in range(1,pas_hg):
                                tablier_local[l-k,c-k] = self.joueur   

                        if isAccessible : 
                            self.liste_coord_successeurs.append([l,c])
                            self.liste_successeurs.append(Othellier(self.prof-1,-self.joueur,tablier_local))
                       


    def successeurs(self):
        # On parcourt toutes les cases de l'othellier
        if self.prof > 0 :     
            i = 0        
            for ligne in self.tablier:       
                j = 0
                for case in ligne:
                    # Dès qu'on trouve une case vide, on teste si elle est accessible par la couleur
                    if case == 0:
                        # On crée un othellier identique à l'othellier considéré
                        # à la différence qu'on joue couleur à la position (i,j)
                        tablier_local = np.array([[0 for i in range (8)] for j in range (8)])
                        num_ligne = 0
                        for ligne_tablier_local in tablier_local:
                            num_col = 0
                            for case_tablier_local in ligne_tablier_local:
                                tablier_local[num_ligne,num_col] = self.tablier[num_ligne,num_col]
                                num_col +=1
                            num_ligne += 1
                        tablier_local[i,j] = self.joueur
                        othellier_local = Othellier(self.prof-1,-self.joueur,tablier_local)
                        #othellier_local.tablier[i,j] = self.joueur

                    # Juste ce qu'il y a en dessous ne marchait pas car quand on modifie oth_local ça modifier self.tablier ensuite
                    # othellier_local = Othellier(self.tablier)
                    # othellier_local.tablier[i,j].couleur = couleur
                    
                    # On va parcourir dans toutes les directions pour voir si il y a des jetons adverses transformables
                    # Si c'est le cas sur au moins 1 ligne ou diagonale --> (i,j) est accessible et on peut ajouter l'othellier construit à la liste des successeurs
                        taille_tablier = 8
                        k = 1 # compteur d'écartement à la position (i,j)
                        continuer_bas, continuer_haut, continuer_droite, continuer_gauche, continuer = True, True, True, True, True
                        continuer_diag_hd, continuer_diag_hg, continuer_diag_bd, continuer_diag_bg = True, True, True, True
                        accessible = False

                    # On parcourt tant que c'est encore possible de trouver une solution --> continuer = True
                        while continuer:
                        # Droite
                            if ((j+k) < taille_tablier) and continuer_droite:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                                if othellier_local.tablier[i,j+k] == self.joueur:
                                    continuer_droite = False
                                    for l in range(1,k):
                                        othellier_local.tablier[i,j+l] = self.joueur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                    if k > 1:
                                        accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                                if othellier_local.tablier[i,j+k] == 0 :
                                    continuer_droite = False
                            else:
                                continuer_droite = False

                        # Gauche
                            if ((j-k) >= 0) and continuer_gauche:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                                if othellier_local.tablier[i,j-k] == self.joueur:
                                    continuer_gauche = False
                                    for l in range(1,k):
                                        othellier_local.tablier[i,j-l] = self.joueur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                    if k > 1:
                                        accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                                if othellier_local.tablier[i,j-k] == 0 :
                                    continuer_gauche = False
                            else:
                                continuer_gauche = False

                        # Bas
                            if ((i+k) < taille_tablier) and continuer_bas:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                                if othellier_local.tablier[i+k,j] == self.joueur:
                                    continuer_bas = False
                                    for l in range(1,k):
                                        othellier_local.tablier[i+l,j] = self.joueur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                    if k > 1:
                                        accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                                if othellier_local.tablier[i+k,j] == 0 :
                                    continuer_bas = False
                            else:
                                continuer_bas = False

                        # Haut
                            if ((i-k) >= 0) and continuer_haut:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                                if othellier_local.tablier[i-k,j] == self.joueur:
                                    continuer_haut = False
                                    for l in range(1,k):
                                        othellier_local.tablier[i-l,j] = self.joueur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                    if k > 1:
                                        accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                                if othellier_local.tablier[i-k,j] == 0 :
                                    continuer_haut = False
                            else:
                                continuer_haut = False
                        
                        # Diagonale Haut-Droite
                            if ((i-k) >= 0) and ((j+k) < taille_tablier) and continuer_diag_hd:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                            
                                if othellier_local.tablier[i-k,j+k] == self.joueur:
                                    continuer_diag_hd = False
                                    for l in range(1,k):
                                        othellier_local.tablier[i-l,j+l] = self.joueur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                    if k > 1:
                                        accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                                if othellier_local.tablier[i-k,j+k] == 0 :
                                    continuer_diag_hd = False
                            else:
                                continuer_diag_hd = False
                        
                        # Diagonale Haut-Gauche
                            if ((i-k) >= 0) and ((j-k) >= 0) and continuer_diag_hg:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                                if othellier_local.tablier[i-k,j-k] == self.joueur:
                                    continuer_diag_hg = False
                                    for l in range(1,k):
                                        othellier_local.tablier[i-l,j-l] = self.joueur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                    if k > 1:
                                        accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                                if othellier_local.tablier[i-k,j-k] == 0 :
                                    continuer_diag_hg = False
                            else:
                                continuer_diag_hg = False
                        
                        # Diagonale Bas-Gauche
                            if ((i+k) < taille_tablier) and ((j-k) >= 0) and continuer_diag_bg:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                                if othellier_local.tablier[i+k,j-k] == self.joueur:
                                    continuer_diag_bg = False
                                    for l in range(1,k):
                                        othellier_local.tablier[i+l,j-l] = self.joueur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                    if k > 1:
                                        accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                                if othellier_local.tablier[i+k,j-k] == 0 :
                                    continuer_diag_bg = False
                            else:
                                continuer_diag_bg = False
                        
                        # Diagonale Bas-Droite
                            if ((i+k) < taille_tablier) and ((j+k) < taille_tablier) and continuer_diag_bd:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                                if othellier_local.tablier[i+k,j+k] == self.joueur:
                                    continuer_diag_bd = False
                                    for l in range(1,k):
                                        othellier_local.tablier[i+l,j+l] = self.joueur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                    if k > 1:
                                        accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                                if othellier_local.tablier[i+k,j+k] == 0 :
                                    continuer_diag_bd = False
                            else:
                                continuer_diag_bd = False
                        

                        # Si on peut encore explore dans au moins l'une des directions, on continue
                            continuer = continuer_bas or continuer_haut or continuer_droite or continuer_gauche or continuer_diag_hd or continuer_diag_hg or continuer_diag_bg or continuer_diag_bd
                            k += 1
                    
                    # Si dans au moins l'une des directions on a pu transformer des pions adverses --> on stocke (i,j) et l'othellier obtenu
                        if accessible:
                            self.liste_coord_successeurs.append([i,j])
                            self.liste_successeurs.append(othellier_local)

                    j += 1
                i +=1

    def evaluate (self):
            #initialisation du score
        pscore = 0
        # pour parcourir les quatres coins 
        for i in [0,2]:
            for j in [0,2]:  
                ligne = int(i * 7/2)
                col = int(j * 7/2)
                # est-il capturé 
                if self.tablier[ligne,col] == self.joueur : 
                    # si oui par moi : 60
                    pscore += 60
                #si il n'est pas capturé    
                elif self.tablier[ligne,col] == 0 : 
                    # est ce que je suis dans les trois autour : -20 pour chaque
                    if self.tablier[ligne + 1 - i,col] == self.joueur : 
                        pscore -= 20
                    if self.tablier[ligne,col + 1 - j] == self.joueur : 
                        pscore -= 20
                    if self.tablier[ligne + 1 - i,col + 1 - j] == self.joueur : 
                        pscore -= 20
        return pscore

    def gagnant(self):
        if self.liste_successeurs == []:
            nb_blanc = 0
            nb_noir = 0
            for ligne in self.tablier:
                for case in ligne:
                    if case == 1:
                        nb_blanc += 1
                    if case == -1:
                        nb_noir += 1
        
            if nb_blanc > nb_noir:
                return 1
            elif nb_blanc < nb_noir:
                return -1
            else:
                return 2
        else : 
            return 0

def MinMax(othellier,prof,joueur,isMaximizing):
    if (prof == 0) : 
        return (othellier.evaluate())
    if othellier.gagnant() == joueur : 
        return 1000
    if othellier.gagnant() == -joueur : 
        return -1000
    if isMaximizing : 
        bestscore = -1000
        for sons in othellier.liste_successeurs : 
            score = MinMax(sons,prof-1,-joueur,False)
            if score > bestscore : 
                bestscore = score
        return bestscore
    else : 
        bestscore = 1000
        for sons in othellier.liste_successeurs : 
            score = MinMax(sons,prof-1,-joueur,True)
            if score < bestscore: 
                bestscore = score
        return bestscore

def compMove(othellier,prof,joueur):
    bestScore = -1000
    bestMove = [0,0]

    for i in range(len(othellier.liste_successeurs)) : 
        sons = othellier.liste_successeurs[i]
        score = MinMax(sons,prof-1,-joueur,False)
        if score > bestScore : 
            bestScore = score
            bestMove = othellier.liste_successeurs[i].tablier
    return bestMove

# Initialisation d'un othellier


def game(prof): 
    tablier_0 = np.array([[0 for i in range (8)] for j in range (8)])
    tablier_0[3,3] = 1
    tablier_0[4,4] = 1
    tablier_0[3,4] = -1
    tablier_0[4,3] = -1
    othellier_0 = Othellier(p_prof,1,tablier_0)
    liste_othellier_partie = [othellier_0]
    i = 0
    joueur = othellier_0.joueur
    while liste_othellier_partie[i].gagnant() == 0 : 
        print(liste_othellier_partie[i].tablier)
        joueur = -joueur
        liste_othellier_partie.append(Othellier(p_prof,joueur,compMove(liste_othellier_partie[i],prof,joueur)))
        i += 1
    print(liste_othellier_partie[i].tablier)
    print('Victoire :')
    print(liste_othellier_partie[i].gagnant())

game(2)
tablier_0 = np.array([[0 for i in range (8)] for j in range (8)])
tablier_0[3,3] = -1
tablier_0[4,4] = 1
tablier_0[3,4] = 1
tablier_0[4,3] = -1
tablier_0[2,4] = 1
tablier_0[2,3] = -1
#othellier_test = Othellier(1,-1,tablier_0)
#print(othellier_test.tablier)
#for o in othellier_test.liste_successeurs :
#print(o.tablier)
#for o in othellier_0.liste_successeurs : 
#    for i in o.liste_successeurs :
#        print (o.tablier)
#        print (i.tablier)