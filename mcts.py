from collections import defaultdict
import profile
import ssl
import numpy as np
from math import *
from tkinter import *
import tkinter as tk
from random import randint, random
import copy as copy


class Othellier(object):

    def __init__(self, prof,joueur,tablier):#,score = 0 ):
        self.prof = prof #profondeur restante à explorer
        self.joueur = joueur # 1 ou -1
        self.tablier = tablier # matrice 8x8 remplie de 1, de -1 et de 0 (cases vides)
        self.liste_successeurs = [] # liste d'instances Othelliers qui sont les successeurs potentiels de cet Othellier
        self.liste_coord_successeurs = [] # liste des coordonnées de la case jouée pour chacun des successeurs
        self.successeurs_bis() # lance la méthode successeurs qui remplie les listes successeurs. 
                                # Cette méthode est donc automatiquement appelée lorsqu'un othellier est crée. 
        #self.successeurs() #idem avec l'autre version de la méthode successeurs
        self.t = 10000 # par défaut au début tous les othelliers ont un UCB = + l'infini
        self.n = 0 # par défaut au début tous les othelliers ont été visités 0 fois

    # Méthode successeurs : 
    # Obj : Trouver et créer les othelliers successeurs potentiels pour un othellier donné. 
    # Pas d'entrée, les attributs de classes suffisent. En sortie, il modifie juste les attributs liste_successeurs et liste_coord_successeurs
    # Cette méthode est en double du coup, il faudrait vraiment vérifier mais normalement elles font exactement la même chose
    def successeurs_bis(self): 

        # On vérifie si on a atteint la profondeur maximum. Si c'est le cas, il faut arrêter la recherche de successeurs.
        # L'idée étant que l'on ne veut pas explorer tout l'arbre. 
        if self.prof > 0 : 

            # Parcours (jsp écrire) du tablier pour trouver les cases vides
            for l in range(8):
                for c in range(8):
                    #Si la case est vide
                    if self.tablier[l,c] == 0 : 

                        #Si on trouve un case vide, on ajoute un jeton dessus, ce qui donne un tablier local modifié
                        #Création du tablier local
                        tablier_local = np.array([[0 for i in range (8)] for j in range (8)])
                        #Remplissage du tablier local de manière identique du tablier d'origine
                        for lbis in range(8):
                            for cbis in range(8):
                                tablier_local[lbis,cbis] = self.tablier[lbis,cbis]
                        #Ajout du jeton sur la case vide
                        tablier_local[l,c] = self.joueur

                        #Est-ce que l'on a le droit de jouer sur cette position ? 
                        #L'idée va être de vérifier dans chaque direction si on à au moins un jeton adverse puis un jeton à nous 

                        #Initialisation de booléen servant à vérifier si des directions autour du point sont explorables
                        isAccessible = False #Booléen général disant si cette case est jouable
                        isAccessibleB = False #Bas est-il explorable ? 
                        isAccessibleBD = False #Bas Droite est-il explorable ? 
                        isAccessibleBG = False #Bas Gauchee st-il explorable ? 
                        isAccessibleG = False #Gauche est-il explorable ? 
                        isAccessibleD = False #Droite est-il explorable ? 
                        isAccessibleH = False #Haut est-il explorable ? 
                        isAccessibleHD = False #Haut Droite est-il explorable ? 
                        isAccessibleHG = False #Haut Gauche est-il explorable ? 

                        #On regarde dans chaque direction : 

                            #BAS
                        #On fixe un pas qui est donc l'écart d'exploration à la case 
                        #On a un pas pour chaque direction parceque l'on va en avoir besoin après pour modifier les jetons
                        pas_b = 1
                        # Tant que c'est des jetons adverses et qu'on ne dépasse pas les bords
                        while pas_b + l < 7 and tablier_local[l+pas_b,c] == -self.joueur :
                            #on continue 
                            pas_b += 1
                        #Si il y avait au moins un jeton adverse et que l'on s'est arrêté sur un jeton à nous
                        if (pas_b > 1) and (tablier_local[l+pas_b,c]== self.joueur) : 
                            #cette direction est accessible
                            isAccessible = True
                            isAccessibleB = True
                    
                            #HAUT
                        #On fixe un pas qui est donc l'écart d'exploration à la case 
                        pas_h = 1
                        # Tant que c'est des jetons adverses et qu'on ne dépasse pas les bords
                        while l - pas_h > 0 and tablier_local[l-pas_h,c] == -self.joueur : 
                            #on continue 
                            pas_h += 1
                        #Si il y avait au moins un jeton adverse et que l'on s'est arrêté sur un jeton à nous
                        if (pas_h > 1) and (tablier_local[l-pas_h,c]== self.joueur) : 
                            #cette direction est accessible
                            isAccessible = True
                            isAccessibleH = True   

                            #GAUCHE
                        #On fixe un pas qui est donc l'écart d'exploration à la case 
                        pas_g = 1
                        # Tant que c'est des jetons adverses et qu'on ne dépasse pas les bords
                        while c - pas_g > 0 and tablier_local[l,c-pas_g] == -self.joueur : 
                            #on continue 
                            pas_g += 1
                        #Si il y avait au moins un jeton adverse et que l'on s'est arrêté sur un jeton à nous
                        if (pas_g > 1) and (tablier_local[l,c-pas_g]== self.joueur) : 
                            #cette direction est accessible
                            isAccessible = True
                            isAccessibleG = True   

                            #DROITE
                        #On fixe un pas qui est donc l'écart d'exploration à la case 
                        pas_d = 1
                        # Tant que c'est des jetons adverses et qu'on ne dépasse pas les bords
                        while c + pas_d < 7 and tablier_local[l,c+pas_d] == -self.joueur : 
                            #on continue 
                            pas_d += 1
                        #Si il y avait au moins un jeton adverse et que l'on s'est arrêté sur un jeton à nous
                        if (pas_d > 1) and (tablier_local[l,c+pas_d]== self.joueur) : 
                            #cette direction est accessible
                            isAccessible = True
                            isAccessibleD = True
                                                                                 
                            #BAS-Gauche
                        #On fixe un pas qui est donc l'écart d'exploration à la case 
                        pas_bg = 1
                        # Tant que c'est des jetons adverses et qu'on ne dépasse pas les bords
                        while pas_bg + l < 7 and c - pas_bg > 0 and tablier_local[l+pas_bg,c-pas_bg] == -self.joueur  : 
                            #on continue 
                            pas_bg += 1
                        #Si il y avait au moins un jeton adverse et que l'on s'est arrêté sur un jeton à nous
                        if (pas_bg > 1) and (tablier_local[l+pas_bg,c-pas_bg]== self.joueur) : 
                            #cette direction est accessible
                            isAccessible = True
                            isAccessibleBG = True
                            
                            #Haut-Droite
                        #On fixe un pas qui est donc l'écart d'exploration à la case 
                        pas_hd = 1
                        # Tant que c'est des jetons adverses et qu'on ne dépasse pas les bords
                        while l - pas_hd > 0 and c + pas_hd < 7 and tablier_local[l-pas_hd,c+pas_hd] == -self.joueur : 
                            #on continue 
                            pas_hd += 1
                        #Si il y avait au moins un jeton adverse et que l'on s'est arrêté sur un jeton à nous
                        if (pas_hd > 1) and (tablier_local[l-pas_hd,c+pas_hd]== self.joueur) : 
                            #cette direction est accessible
                            isAccessible = True
                            isAccessibleHD = True  

                            #GAUCHE-Haut
                        #On fixe un pas qui est donc l'écart d'exploration à la case 
                        pas_hg = 1
                        # Tant que c'est des jetons adverses et qu'on ne dépasse pas les bords
                        while c - pas_hg > 0 and l - pas_hg > 0  and tablier_local[l-pas_hg,c-pas_hg] == -self.joueur :
                            #on continue  
                            pas_hg += 1
                        #Si il y avait au moins un jeton adverse et que l'on s'est arrêté sur un jeton à nous
                        if (pas_hg > 1) and (tablier_local[l-pas_hg,c-pas_hg]== self.joueur) : 
                            #cette direction est accessible
                            isAccessible = True
                            isAccessibleHG = True
                             
                            #DROITE-Bas
                        #On fixe un pas qui est donc l'écart d'exploration à la case 
                        pas_bd = 1
                        # Tant que c'est des jetons adverses et qu'on ne dépasse pas les bords
                        while c + pas_bd < 7 and pas_bd + l < 7 and tablier_local[l+pas_bd,c+pas_bd] == -self.joueur : 
                            #on continue 
                            pas_bd += 1
                        #Si il y avait au moins un jeton adverse et que l'on s'est arrêté sur un jeton à nous
                        if (pas_bd > 1) and (tablier_local[l+pas_bd,c+pas_bd]== self.joueur) : 
                            #cette direction est accessible
                            isAccessible = True
                            isAccessibleBD = True
                            
                        #Maintenant, il faut modifier le plateau : retourner les jetons capturés
                        #On ne le fait pas au même moment que l'exploration car il ne faut pas que les jetons nouvellement capturés soit pris en compte à ce tour là. 
                        #Pour chaque direction, si elle était acccessible : on met le numéro du joueur (1 ou -1) sur les cases adverses
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

                        #On crée un othellier et on l'ajoute à l'attribut liste_successeurs, ainsi que les coordonnées de la case jouée à liste_coord_successeurs
                        if isAccessible : 
                            self.liste_coord_successeurs.append([l,c])
                            # L'othellier que l'on crée à donc un profondeur à explorer plus faible (d'où le prof-1), et ce sera le tour de l'autre joueur (d'où le -self.joueur)
                            # On remarque que lorsque l'on va crée cet Othellier, il va aussi appeler cette méthode pour aller chercher ses successeurs. 
                            # Et si il en a, ses successeurs vont eux même appelé cette méthode et ainsi de suite jusqu'à la profondeur max ou jusqu'à atteindre des othelliers terminaux (gagnant ou perdant) 
                            self.liste_successeurs.append(Othellier(self.prof-1,-self.joueur,tablier_local))
                        #Si la case n'était pas accessible/jouable, rien n'est ajouté aux listes successeurs
        else : 
            #Si on a atteint la profondeur max, on l'indique. Il ne faut pas rien faire 
            # car sinon ça donnerai une liste vide dans les listes successeurs et on serait incapable de différencier ce cas du cas où l'on n'a pas toruvé de successeur.
            self.liste_coord_successeurs = ['profmax']
            self.liste_successeurs = ['profmax']
                       

    #fait comme successeurs_bis mais d'une manière un peu différente
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
    #fonction d'évaluation
    #En sortie : le score d'évaluation de cet othellier
    #Pour l'instant elle est basé uniquement sur l'occupation des coins. 
    #Un coin capturé vaut 60. 
    #Un jeton autour d'un coin non-capturé vaut -20 car ça donne l'opportunité à l'autre joueur de capturer le coin
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

    #Méthode disant si il est encore possible de jouer sur cet othellier pour le joueur concerné. 
    #Si oui, elle renvoit 0
    #Sinon, elle compte les pions et renvoie celui qui a le plus de jeton sur l'othellier (2 si égalité)
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



##########Fonction MinMax#################
#Cette fonction va faire remonter le valeur d'une branche
#Elle fonctionne par recursion jusqu'à atteindre soit la profondeur max d'exploration, soit un othellier terminal
#La recursion alterne entre des étages min et des étages max
def MinMax(othellier,prof,joueur,isMaximizing):

    #Conditions d'arrêts et scores à remonter 

    #Si l'othellier est gagnant, on remonte un valeur très élevé 1000
    if othellier.gagnant() == joueur : 
        return 1000
    #Si il est perdant, on remonte une valeur très faible -1000
    if othellier.gagnant() == -joueur : 
        return -1000
    #Si l'othellier n'est pas terminal, et que l'on a atteint la profondeur max: 
    # on s'arrête et on utilise la fonction d'evaluation pour connaitre le score à remonter
    if (prof == 0) : 
        return (othellier.evaluate())

    #Tant que l'on est dans aucun de ces cas : 
    #Si on est sur un noeud max 
    if isMaximizing : 
        bestscore = -10000
        #Pour chaque successeurs, on relance MinMax
        for sons in othellier.liste_successeurs : 
            #On était sur un noeud max, les noeuds successeurs seront donc des noeuds min
            score = MinMax(sons,prof-1,-joueur,False) #recursion
            #On remonte le score maximal
            if score > bestscore : 
                bestscore = score
        return bestscore
    #Si on est sur un noeud min
    else : 
        bestscore = 10000
        #Pour chaque successeurs, on relance MinMax
        for sons in othellier.liste_successeurs : 
            #On était sur un noeud min, les noeuds successeurs seront donc des noeuds max
            score = MinMax(sons,prof-1,-joueur,True) #recursion
            #On remonte le score minimal
            if score < bestscore: 
                bestscore = score
        return bestscore

########################## MCTS ###########################

def MCTS(othellier, prof, passe, C, T, i): # j'ai mis T ici dans l'idée qu'on va mettre la fonction MCTS en boucle avec un T qui augmente en dehors de l'appel de fonction
    ### Si on est au tout début du jeu, on va choisir l'othellier suivant au hasard car aucun othellier n'a été visité donc tous les UCB valent + l'infini
    #if othellier == othellier_0:
    if i == 0:
        # choix d'un othellier successeur au hasard puisque toutes les valeurs d'UCB valent + l'infini
        othelliers_choisis = [othellier]
        # ici au lieu de juste aller a prof max on voudrait aussi avoir une condition sur passe, un truc du genre
        # while prof_i < othellier.prof+1 OR passe < 2: (avec incrémentation de prof_i) mais pas encore sure de comment faire fonctionner ça
        prof_i = 1
        print("valeur passe", passe)
        while (prof_i < othellier.prof+1) : # on parcourt jusqu'en bas de la profondeur de l'othellier choisi ou jusqu'à ce que la partie se finisse 
            othellier_pere = othellier # l'othellier au rang i est le père de l'othellier au rang i+1
            othellier_pere.n += 1 # on a visité cet othelier une fois
            nbr_successeurs = len(othellier_pere.liste_successeurs) # parmi combien de successeurs doit-on choisir
            othellier_choisi = randint(0,nbr_successeurs-1) # choix au hasard
            othellier = othellier.liste_successeurs[othellier_choisi] # 
            othelliers_choisis.append(othellier) # on enregistre les othelliers par lesquels on passe pour actualiser leurs scores n ensuite
            othellier.n += 1 # on est passé par cet othellier
            prof_i += 1

        joueur = othellier.joueur # savoir de quel joueur on part
        othellier_final = game_MCTS(othellier, 1, joueur)
        othellier.t = 0
        if othellier_final.gagnant() == joueur: # si ce joueur gagne la partie
            score = 1
            if othellier.t == 10000:
                othellier.t = score # l'othellier duquel le jeu est parti prend 1
            else:
                othellier.t += score
        else:
            score = -1
            if othellier.t == 10000:
                othellier.t = score
            else:
                othellier.t += score # en cas de défaite
    
    else:
        print("valeur passe", passe)

        othelliers_choisis = [othellier]
        prof_i=1
        while (prof_i < othellier.prof+1): # aller choisir l'othellier le plus prometteur parmi tous les successeurs possibles sur une profondeur donnée de l'othellier de départ
            othellier_pere = othellier
            othellier_pere.n += 1
            
            # là on va regarder les valeurs d'UCB des successeurs, mais s'ils n'ont pas été visité leur n vaudra 10000 donc on vérifie
            # si plusieurs n'ont pas été visités ils auront forcément tous des valeurs d'UCB infinie donc on prendra au hasard parmi ceux encore non visités
            # s'ils ont tous été visités on prend la valeur max des UCB 

            liste_scores_successeurs = []
            for successeur in othellier_pere.liste_successeurs:
                if successeur.n != 0: # si le noeud a été vu au moins une fois
                    liste_scores_successeurs.append(successeur.t/successeur.n + C * np.sqrt(np.log(T)/successeur.n)) # calcul de l'UCB
                else:
                    liste_scores_successeurs.append(successeur.t)
                
            successeur_choisi = np.argmax(liste_scores_successeurs) # retourne l'indice de l'UCB le plus élevé, les successeurs 
                                                                 # étant parcourus dans l'ordre on sait à quel successeur ça correspond
            othellier_choisi = othellier_pere.liste_successeurs[successeur_choisi]
            othellier_choisi.n += 1 # l'othellier choisi est visité une fois
            othelliers_choisis.append(othellier_choisi) # ajouté à la liste des othelliers visités
            
            othellier = othellier_choisi 
            prof_i += 1
        
        joueur = othellier.joueur # maintenant qu'on sait de quel othellier on part on sait qui joue et on peut lancer la partie aléatoire
        othellier_final = game_MCTS(othellier, 1, joueur)    
        if othellier_final.gagnant() == joueur: # si ce joueur gagne la partie
            score = 1
            if othellier.t == 10000:
                othellier.t = score # l'othellier duquel le jeu est parti prend 1
            else:
                othellier.t += score
        else:
            score = -1
            if othellier.t == 10000:
                othellier.t = score
            else:
                othellier.t += score # en cas de défaite
        
    # maintenant on veut faire remonter l'information sur la victoire/défaite après la partie aléatoire grâce à la liste othelliers_choisis
    for othellier in othelliers_choisis:
        if othellier.t == 10000:
            othellier.t = score
        else:
            othellier.t += score # tous les othelliers qui ont été choisis pour arriver à l'othellier duquel la partie aléatoire a été lancée ont leur score modifié
        print("scores t", othellier.t)
    print("score n", othelliers_choisis[0].n, othelliers_choisis[0])
    print("score t de 0", othelliers_choisis[0].t)
    print("score n de 0 devrait être = à T", othelliers_choisis[0].n)

## jeu aléatoire partant d'un othellier prédterminé

def game_MCTS(othellier, prof, joueur):
    print("jeu aléatoire MCTS")
    tablier_0 = othellier.tablier
    othellier_0 = Othellier(prof, joueur, tablier_0)
    liste_othellier_partie = [othellier_0]

    #initialisations
    i = 0 #compteur de tour
    joueur = othellier_0.joueur #A qui le tour ? 
    passe = 0 #compte le nombre de tours passés successifs
    #Boucle de jeu
    while passe<2 : #si les deux joueurs passent successivement, c'est qu'on ne peut plus jouer, on arrête
        if liste_othellier_partie[i].gagnant() == 0: #Si il peut jouer
            print("joue")
            #Il joue : création de l'othellier suivant en récuperant la grille après que le joueur ait joué par la fonction compMove
            #On change bien le joueur dans le nouvel othellier crée (-joueur)
            nbr_successeurs = len(liste_othellier_partie[i].liste_successeurs)
            successeur_aleatoire = liste_othellier_partie[i].liste_successeurs[randint(0, nbr_successeurs-1)]
            liste_othellier_partie.append(Othellier(1, -joueur, successeur_aleatoire.tablier)) 
            #On n'a pas passé, passe revient à 0
            passe = 0
        else : #On ne peut pas jouer
            print('passe')
            passe += 1 #On compte que l'on a passé
            liste_othellier_partie.append(Othellier(prof,-joueur,liste_othellier_partie[i].tablier)) #On ajoute le même othellier mais avec pour joueur l'autre joueur
        joueur = -joueur #changement de joueur
        i += 1
        othellier_0 = liste_othellier_partie[i]
    return(liste_othellier_partie[-1]) # besoin de récupérer le dernier othellier pour savoir qui gagne

###################Fonction de choix du prochain move de l'ordi########################
#Prend en entrée un othellier, la profondeur max d'exploration et le joueur qui joue 
#En sortie : le tablier resultant du move qu'il a fait
def compMove(othellier,prof,joueur):

    #On initialise le score max à une valeur très basse
    bestScore = -10000
    #On initialise le tablier de sortie comme on veut
    bestMove = np.array([[0 for i in range (8)] for j in range (8)])

    #On va parcourir les successeurs de l'othellier actuel
    #C'est un de ces successeurs que l'on va choisir, il faut donc les évaluer
    for i in range(len(othellier.liste_successeurs)) : 
        sons = othellier.liste_successeurs[i]

        #On les evaluent avec la fonction MinMax qui va s'occuper de faire remonter la valeur de l'othellier successeur
        #On est donc un étage plus bas sur l'arbre que l'othellier initial (d'où prof-1)
        #On est sur un étage Max, le prochain sera donc un étage Min (d'où le -joueur et False)
        score = MinMax(sons,prof-1,-joueur,False)

        #Ici, on cherche à maximiser le score du joueur, donc si le score dépasse le score max jusqu'à là :  
        # On change le best score et on retient le tablier du successeurs qui a ce nouveau score max
        if score > bestScore : 
            bestScore = score
            bestMove = othellier.liste_successeurs[i].tablier
    return bestMove

## pour tester MCTS

def compMoveMCTS(othellier,prof,joueur, passe, i):

    #On initialise le score max à une valeur très basse
    bestScore = -10000
    #On initialise le tablier de sortie comme on veut
    bestMove = np.array([[0 for i in range (8)] for j in range (8)])

    for T in range(3): # on fait T fois le processus de MCTS
        MCTS(othellier, prof, passe, 2, T, i)

    #On va parcourir les successeurs de l'othellier actuel
    #C'est un de ces successeurs que l'on va choisir, il faut donc les évaluer
    for i in range(len(othellier.liste_successeurs)) : 
        sons = othellier.liste_successeurs[i]

        scores = [sons.t for k in range(len(othellier.liste_successeurs))]
        if len(scores) == 0:
            print('Partie finie')
        else:
            score_max = max(scores)
            where_score_max = np.argmax(scores)

        #Ici, on cherche à maximiser le score du joueur, donc si le score dépasse le score max jusqu'à là :  
        # On change le best score et on retient le tablier du successeurs qui a ce nouveau score max
        if score_max > bestScore : 
            bestScore = score_max
            bestMove = othellier.liste_successeurs[where_score_max].tablier
    return bestMove


#####################Fonction globale de jeu###########################
#Lance un partie pour une profondeur max d'exploration donnée.
def game(prof): 

    #Création de l'othellier initial
    tablier_0 = np.array([[0 for i in range (8)] for j in range (8)])
    tablier_0[3,3] = 1
    tablier_0[4,4] = 1
    tablier_0[3,4] = -1
    tablier_0[4,3] = -1
    #On commence par le joueur 1, c'est arbitraire
    othellier_0 = Othellier(prof,1,tablier_0)

    #Initialisation de liste retenant les othelliers joués (peut-être un peu lourd de tous les retenir, en soit il suffit d'en retenir un seul donc on pourra changer)
    liste_othellier_partie = [othellier_0]
    #initialisations
    i = 0 #compteur de tour
    joueur = othellier_0.joueur #A qui le tour ? 
    passe = 0 #compte le nombre de tours passés successifs
    #Boucle de jeu
    while passe<2 : #si les deux joueurs passent successivement, c'est qu'on ne peut plus jouer, on arrête
        print(joueur)
        print("tablier", liste_othellier_partie[i].tablier)
        if liste_othellier_partie[i].gagnant() == 0 : #Si il peut jouer
            print('joue')
            #Il joue : création de l'othellier suivant en récuperant la grille après que le joueur ait joué par la fonction compMove
            #On change bien le joueur dans le nouvel othellier crée (-joueur)
            #liste_othellier_partie.append(Othellier(prof,-joueur,compMove(liste_othellier_partie[i],prof,joueur))) 
            liste_othellier_partie.append(Othellier(prof,-joueur,compMoveMCTS(liste_othellier_partie[i],prof,joueur,passe,i))) 
            #On n'a pas passé, passe revient à 0
            passe = 0
        else : #On ne peut pas jouer
            print('passe')
            passe += 1 #On compte que l'on a passé
            liste_othellier_partie.append(Othellier(prof,-joueur,liste_othellier_partie[i].tablier)) #On ajoute le même othellier mais avec pour joueur l'autre joueur
        joueur = -joueur #changement de joueur
        i += 1
    print("tablier final", liste_othellier_partie[i].tablier)
    print('Victoire :')
    print("joueur", liste_othellier_partie[i].gagnant())

####Test######
game(4)
#tablier_0 = np.array([[0 for i in range (8)] for j in range (8)])
#tablier_0[3,3] = 1
#tablier_0[4,4] = 1
#tablier_0[3,4] = 1
#tablier_0[4,3] = -1
#tablier_0[2,4] = 1
#tablier_0[2,3] = 0
#othellier_test = Othellier(3,1,tablier_0)
#print(othellier_test.tablier)
#for o in othellier_test.liste_successeurs :
#    print (o.tablier)
#    print(o.liste_successeurs) 
#    for i in o.liste_successeurs :
#        print (i.tablier)