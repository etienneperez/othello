import profile
import ssl
import numpy as np
from math import *
from tkinter import *
import tkinter as tk
from random import randint, random
import copy as copy


class Othellier(object):

    def __init__(self, prof,joueur,tablier, passe = FALSE):#,score = 0 ):
        self.prof = prof #profondeur restante à explorer
        self.joueur = joueur # 1 ou -1
        self.tablier = tablier # matrice 8x8 remplie de 1, de -1 et de 0 (cases vides)
        self.liste_successeurs = [] # liste d'instances Othelliers qui sont les successeurs potentiels de cet Othellier
        self.liste_coord_successeurs = [] # liste des coordonnées de la case jouée pour chacun des successeurs
        self.gagnant = 0
        self.precedent_passe = passe
        self.successeurs_bis() # lance la méthode successeurs qui remplie les listes successeurs. 
                                # Cette méthode est donc automatiquement appelée lorsqu'un othellier est crée. 
        #self.successeurs() #idem avec l'autre version de la méthode successeurs
        self.score = 0 # utile dans alpha-beta pour retrouver quel othellier a telle valeur d'alpha

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
                        #L'idée va être de vérifier dans chaque difrection si on à au moins un jeton adverse puis un jeton à nous 

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
            
            # Si pas de successeurs, alors le joueur passe son tour = il joue ce même othellier et on change joueur
            if self.liste_successeurs == [] and not self.precedent_passe : 
                self.liste_successeurs = [Othellier(self.prof-1,-self.joueur,self.tablier,TRUE)]
            # Si pas de successeur, et que le joueur adverse avait déjà passé avant = partie finie
            if self.liste_successeurs == [] and self.precedent_passe : 
                self.isGagnant()
        else : 
            #Si on a atteint la profondeur max, on l'indique. Il ne faut pas rien faire 
            # car sinon ça donnerai une liste vide dans les listes successeurs et on serait incapable de différencier ce cas du cas où l'on n'a pas toruvé de successeur.
            self.liste_coord_successeurs = ['profmax']
            self.liste_successeurs = ['profmax']
                       
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

    #Méthode disant si il est encore possible de jouer sur cet othellier pour le joueur concerné ET si le joueur adversaire peut aussi jouer le coup d'après si on passe
    #Si oui, elle renvoit 0
    #Sinon, elle compte les pions et renvoie celui qui a le plus de jeton sur l'othellier (2 si égalité)
    def isGagnant(self):
                                                                            # prob = ça prend bcp de temps d'initialiser un 2ème othellier à chaque fois qu'on appelle gagnant
        nb_blanc = 0
        nb_noir = 0
        for ligne in self.tablier:
            for case in ligne:
                if case == 1:
                    nb_blanc += 1
                if case == -1:
                    nb_noir += 1
    
        if nb_blanc > nb_noir:
            self.gagnant = 1
        elif nb_blanc < nb_noir:
            self.gagnant =  -1
        else:
            self.gagnant =  2
    
        
    
    

##########Fonction MinMax#################
#Cette fonction va faire remonter le valeur d'une branche
#Elle fonctionne par recursion jusqu'à atteindre soit la profondeur max d'exploration, soit un othellier terminal
#La recursion alterne entre des étages min et des étages max
def MinMax(othellier,prof,joueur,isMaximizing):
    #Conditions d'arrêts et scores à remonter 
    if othellier.precedent_passe == True and othellier.liste_successeurs == []:
        return 1000
    #Si l'othellier est gagnant, on remonte un valeur très élevé 1000
    if othellier.gagnant == joueur : 
        return 1000
    #Si il est perdant, on remonte une valeur très faible -1000
    if othellier.gagnant == -joueur : 
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
        for son in othellier.liste_successeurs : 
            #On était sur un noeud max, les noeuds successeurs seront donc des noeuds min
            score = MinMax(son,prof-1,-joueur,False) #recursion
            #On remonte le score maximal
            if score > bestscore : 
                bestscore = score
        return bestscore
    #Si on est sur un noeud min
    else : 
        bestscore = 10000
        #Pour chaque successeurs, on relance MinMax
        for son in othellier.liste_successeurs : 
            #On était sur un noeud min, les noeuds successeurs seront donc des noeuds max
            score = MinMax(son,prof-1,-joueur,True) #recursion
            #On remonte le score minimal
            if score < bestscore: 
                bestscore = score
        return bestscore


##########Fonction AlphaBeta #################
#Cette fonction va faire remonter le valeur d'une branche --> on prendra le max pour choisir quoi jouer
#Elle fonctionne par recursion jusqu'à atteindre soit la profondeur max d'exploration, soit un othellier terminal
#La recursion alterne entre des étages min et des étages max
def AlphaBeta(othellier,prof,joueur,alpha,beta,isMaximizing):

    # Si la partie se finit (2 joueurs sans successeurs d'affillée)
    if othellier.precedent_passe == True and othellier.liste_successeurs == []:
        othellier.score = 1000
        return 1000
    #Si l'othellier est gagnant, on remonte un valeur très élevé 1000
    if othellier.gagnant == joueur :
        othellier.score = 1000
        return 1000
    #Si il est perdant, on remonte une valeur très faible -1000
    if othellier.gagnant == -joueur : 
        othellier.score = -1000
        return -1000

    #Si l'othellier n'est pas terminal, et que l'on a atteint la profondeur max ou qu'il n'y a pas de successeur: 
    # on s'arrête et on utilise la fonction d'evaluation pour connaitre le score à remonter
    # Le cas liste_succes == [] = l'oth n'a pas de succes mais n'est pas gagnant ou perdant car l'avdersaire peut jouer au coup d'après
    if (prof == 0) or (othellier.liste_successeurs == []): 
        othellier.score = othellier.evaluate()
        return othellier.score

    #Si on est sur un noeud max 
    if isMaximizing: 
        #Pour chaque successeurs, on relance AlphaBeta
        for son in othellier.liste_successeurs :
            alpha = max(alpha,AlphaBeta(son,prof-1,-joueur,alpha,beta,False))
            if alpha >= beta : 
                break
        return alpha
    #Si on est sur un noeud min
    else: 
        #Pour chaque successeurs, on relance AlphaBeta
        for son in othellier.liste_successeurs : 
            beta = min(beta,AlphaBeta(son,prof-1,-joueur,alpha,beta,True))
            if beta <= alpha:
                break
        return beta


###################Fonction de choix du prochain move de l'ordi pour ALPHA BETA########################
#Prend en entrée un othellier, la profondeur max d'exploration et le joueur qui joue 
#En sortie : le tablier resultant du move qu'il a fait
def compMoveAlphaBeta(othellier,prof,joueur):

    # Pour gérer le cas où il n'y a qu'1 seul successeur possible on le joue direct
    # Gère aussi le cas où celui d'avant a precedent_passe = True --> la partie va se finir car il a gagnant = 1 ou -1
    if len(othellier.liste_successeurs) == 1:

        return Othellier (prof,-joueur,othellier.liste_successeurs[0].tablier,othellier.liste_successeurs[0].precedent_passe)

    # Pour gérer le cas où prof = 1 --> on retourne juste le max des successeurs
    if prof == 1:
        best_score = 0
        bestMove = othellier.liste_successeurs[0].tablier
        ppasse = False
        for son in othellier.liste_successeurs:
            # Si un oth successeur est gagnant, on le joue
            if son.gagnant == joueur :
                othellier.score = 1000
                return son.tablier
            # Si un oth successeur est gagnant pour l'adversaire, on ne le joue surtout pas
            elif son.gagnant == -joueur : 
                son.score = -1000
            else:
                son.score = son.evaluate()
            
            if son.score > best_score:
                best_score = son.score
                bestMove = son.tablier
                ppasse = son.precedent_passe
        return Othellier(prof,-joueur,bestMove,ppasse)

    # Initialisation de alpha et beta
    alpha = -100000000
    beta = 100000000
    ppasse = False
    # On lance alpha-beta qui retourne le score de l'othellier cible vers lequel on doit aller
    score_alpha_beta = AlphaBeta(othellier,prof,joueur,alpha,beta,True)
    # On détermine quel othellier jouer pour être sur la branche qui mène à l'othellier cible dont le score est score_alpha_beta
    for othellier_a_jouer in othellier.liste_successeurs:
        liste_successeurs_prof_i = othellier_a_jouer.liste_successeurs
        
        for i in range(1,prof): # il faut faire prof-2 fois la boucle en gros, sinon après on atteint les feuilles et le calcul des successeurs fait une erreur. Donc 
                                # donc on fait prof-1 fois la boucle et on met une condition sur le calcul des successeurs.
            liste_successeurs_prof_i_plus_1 = []
            for successeur in liste_successeurs_prof_i:
                if successeur.score == score_alpha_beta:
                    return Othellier(prof,-joueur,othellier_a_jouer.tablier,othellier_a_jouer.precedent_passe)
                if i < prof-1: # cf explication plus haut, pour la dernière profondeur, one ne veut pas calculer les successeurs
                    for successeur_de_successeur in successeur.liste_successeurs:
                        liste_successeurs_prof_i_plus_1.append(successeur_de_successeur)
            liste_successeurs_prof_i = liste_successeurs_prof_i_plus_1.copy()



###################Fonction de choix du prochain move de l'ordi########################
#Prend en entrée un othellier, la profondeur max d'exploration et le joueur qui joue 
#En sortie : le tablier resultant du move qu'il a fait
def compMove(othellier,prof,joueur):

    #On initialise le score max à une valeur très basse
    bestScore = -10000
    #On initialise le tablier de sortie comme on veut
    bestMove = np.array([[0 for i in range (8)] for j in range (8)])
    ppasse = FALSE

    #On va parcourir les successeurs de l'othellier actuel
    #C'est un de ces successeurs que l'on va choisir, il faut donc les évaluer
    for son in othellier.liste_successeurs: 
        #On les evaluent avec la fonction MinMax qui va s'occuper de faire remonter la valeur de l'othellier successeur
        #On est donc un étage plus bas sur l'arbre que l'othellier initial (d'où prof-1)
        #On est sur un étage Max, le prochain sera donc un étage Min (d'où le -joueur et False)
        # print("prof :",prof)
        score = MinMax(son,prof-1,-joueur,False)
        # print("score",score)
        #Ici, on cherche à maximiser le score du joueur, donc si le score dépasse le score max jusqu'à là :  
        # On change le best score et on retient le tablier du successeurs qui a ce nouveau score max
        if score > bestScore : 
            bestScore = score
            bestMove = son.tablier
            ppasse = son.precedent_passe
    # Idée = on a la double info de ppasse et de prof.
    # Car si on retourne un successeur, perd de la prof au fur et à mesure des tours
    # print("return Othellier(prof,-joueur,bestMove,ppasse).precedent_passe",Othellier(prof,-joueur,bestMove,ppasse).precedent_passe)
    # print("return Othellier(prof,-joueur,bestMove,ppasse).gagnant",Othellier(prof,-joueur,bestMove,ppasse).gagnant)
    return Othellier(prof,-joueur,bestMove,ppasse)


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
    i = 0 #compteur de tour
    joueur = othellier_0.joueur #A qui le tour ? 

    while liste_othellier_partie[i].gagnant == 0 : #si les deux joueurs passent successivement, c'est qu'on ne peut plus jouer, on arrête
        liste_othellier_partie.append(compMoveAlphaBeta(liste_othellier_partie[i],prof,joueur))
        joueur = -joueur #changement de joueur
        i += 1
    
    print(liste_othellier_partie[i].tablier)
    print('Victoire :')
    print(liste_othellier_partie[i].gagnant)

####Test######
game(3)
