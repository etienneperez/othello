## IMPORTATIONS PREALABLES
import ssl
import numpy as np
from math import *
from tkinter import *
import tkinter as tk
from random import randint, random
import copy as copy
from fonction_evaluation import evaluate_corner, hasard
# from PIL import ImageTk, Image


## Définition des classes

class Case(object):

    def __init__(self, couleur):
        self.couleur = couleur # Valeurs possibles : noir / blanc / vide
    
    # Méthode mettant à jour le statut des cases quand un coup est joué
    def maj_statut(self, couleur = "blanc", ):
        pass

    def __str__(self):
        return str(self.couleur)


class Othellier(object):

    def __init__(self, tablier = 0):
        self.tablier = tablier # matrice 8x8 contenant les Cases
        self.liste_successeurs = [] # liste des noms des successeurs
        self.score = 0 # valeur de la fonction d'évaluation ou max/min des successeurs
        # self.joueur = joueur # "blanc" si c'est au joueur blanc de jouer, "noir" sinon

    # A garder pour quand on aura les cases dans le tablier --> ça affiche une matrice de statuts
    # def __str__(self):
    #     matrice_affichage = np.array([[self.tablier[i,j].statut for i in range (8)] for j in range (8)])
    #     return str(matrice_affichage)
    def __str__(self):
        return str(self.tablier[0,0])

    # Afficher le tablier avec les couleurs de chaque casser
    def afficher(self):
        tablier_affichage = np.array([["abcde" for i in range(8)] for j in range(8)])
        i = 0
        for ligne in self.tablier:
            j = 0
            for case in ligne:
                tablier_affichage[i,j] = case.couleur
                j += 1
            i += 1
        print(tablier_affichage)
    
    # Retourne blanc s'il y a plus de pions blancs que noirs.
    def gagnant(self):
        nb_blanc = 0
        nb_noir = 0
        for ligne in self.tablier:
            for case in ligne:
                if case.couleur == "blanc":
                    nb_blanc += 1
                if case.couleur == "noir":
                    nb_noir += 1
        
        if nb_blanc > nb_noir:
            return "blanc"
        elif nb_blanc < nb_noir:
            return "noir"
        else:
            return "egalite"
    
    # Retourne True s'il n'y a plus de successeurs possibles
    def terminal(self,couleur):
        if self.successeurs(couleur)[1] == []:
            return True
        return False

    # Cette méthode retourne les positions où le joueur peut jouer et les othelliers successeurs correspondant à chaque coup
    # Entrée : 1 othellier, couleur jouée
    # Sortie : 2 listes : 1ère = 2 coord de la case accessible, 2ème = instances d'othellier correspondant à l'othellier obtenu en jouant sur chaque position
    def successeurs(self,couleur):
        
        # On parcourt toutes les cases de l'othellier
        liste_positions_accessibles = []
        liste_successeurs = []
        i = 0
        for ligne in self.tablier:
            j = 0
            for case in ligne:
                # Dès qu'on trouve une case vide, on teste si elle est accessible par la couleur
                if case.couleur == "vide":
                    
                    
                    # On crée un othellier identique à l'othellier considéré
                    # à la différence qu'on joue couleur à la position (i,j)
                    tablier_local = np.array([[Case("vide") for i in range (8)] for j in range (8)])
                    num_ligne = 0
                    for ligne_tablier_local in tablier_local:
                        num_col = 0
                        for case_tablier_local in ligne_tablier_local:
                            tablier_local[num_ligne,num_col].couleur = self.tablier[num_ligne,num_col].couleur
                            num_col +=1
                        num_ligne += 1

                    othellier_local = Othellier(tablier_local)
                    othellier_local.tablier[i,j].couleur = couleur

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
                            if othellier_local.tablier[i,j+k].couleur == couleur:
                                continuer_droite = False
                                for l in range(k):
                                    othellier_local.tablier[i,j+l].couleur = couleur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                if k > 1:
                                    accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                            if othellier_local.tablier[i,j+k].couleur == "vide":
                                continuer_droite = False
                        else:
                            continuer_droite = False

                        # Gauche
                        if ((j-k) >= 0) and continuer_gauche:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                            if othellier_local.tablier[i,j-k].couleur == couleur:
                                continuer_gauche = False
                                for l in range(k):
                                    othellier_local.tablier[i,j-l].couleur = couleur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                if k > 1:
                                    accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                            if othellier_local.tablier[i,j-k].couleur == "vide":
                                continuer_gauche = False
                        else:
                            continuer_gauche = False

                        # Bas
                        if ((i+k) < taille_tablier) and continuer_bas:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                            if othellier_local.tablier[i+k,j].couleur == couleur:
                                continuer_bas = False
                                for l in range(k):
                                    othellier_local.tablier[i+l,j].couleur = couleur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                if k > 1:
                                    accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                            if othellier_local.tablier[i+k,j].couleur == "vide":
                                continuer_bas = False
                        else:
                            continuer_bas = False

                        # Haut
                        if ((i-k) >= 0) and continuer_haut:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                            if othellier_local.tablier[i-k,j].couleur == couleur:
                                continuer_haut = False
                                for l in range(k):
                                    othellier_local.tablier[i-l,j].couleur = couleur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                if k > 1:
                                    accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                            if othellier_local.tablier[i-k,j].couleur == "vide":
                                continuer_haut = False
                        else:
                            continuer_haut = False
                        
                        # Diagonale Haut-Droite
                        if ((i-k) >= 0) and ((j+k) < taille_tablier) and continuer_diag_hd:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                            
                            if othellier_local.tablier[i-k,j+k].couleur == couleur:
                                continuer_diag_hd = False
                                for l in range(k):
                                    othellier_local.tablier[i-l,j+l].couleur = couleur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                if k > 1:
                                    accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                            if othellier_local.tablier[i-k,j+k].couleur == "vide":
                                continuer_diag_hd = False
                        else:
                            continuer_diag_hd = False
                        
                        # Diagonale Haut-Gauche
                        if ((i-k) >= 0) and ((j-k) >= 0) and continuer_diag_hg:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                            if othellier_local.tablier[i-k,j-k].couleur == couleur:
                                continuer_diag_hg = False
                                for l in range(k):
                                    othellier_local.tablier[i-l,j-l].couleur = couleur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                if k > 1:
                                    accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                            if othellier_local.tablier[i-k,j-k].couleur == "vide":
                                continuer_diag_hg = False
                        else:
                            continuer_diag_hg = False
                        
                        # Diagonale Bas-Gauche
                        if ((i+k) < taille_tablier) and ((j-k) >= 0) and continuer_diag_bg:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                            if othellier_local.tablier[i+k,j-k].couleur == couleur:
                                continuer_diag_bg = False
                                for l in range(k):
                                    othellier_local.tablier[i+l,j-l].couleur = couleur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                if k > 1:
                                    accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                            if othellier_local.tablier[i+k,j-k].couleur == "vide":
                                continuer_diag_bg = False
                        else:
                            continuer_diag_bg = False
                        
                        # Diagonale Bas-Droite
                        if ((i+k) < taille_tablier) and ((j+k) < taille_tablier) and continuer_diag_bd:
                            # Dès qu'on tombe sur la même couleur on convertit tous ceux entre les 2 en la couleur et on arrête de chercher dans ce sens
                            if othellier_local.tablier[i+k,j+k].couleur == couleur:
                                continuer_diag_bd = False
                                for l in range(k):
                                    othellier_local.tablier[i+l,j+l].couleur = couleur
                                # Si on tombe sur couleur avec k>1 --> cela signifie que le case est accessible
                                if k > 1:
                                    accessible = True
                            # Si on tombe sur une case vide, on arrête de chercher dans ce sens
                            if othellier_local.tablier[i+k,j+k].couleur == "vide":
                                continuer_diag_bd = False
                        else:
                            continuer_diag_bd = False
                        

                        # Si on peut encore explore dans au moins l'une des directions, on continue
                        continuer = continuer_bas or continuer_haut or continuer_droite or continuer_gauche or continuer_diag_hd or continuer_diag_hg or continuer_diag_bg or continuer_diag_bd
                        k += 1
                    
                    # Si dans au moins l'une des directions on a pu transformer des pions adverses --> on stocke (i,j) et l'othellier obtenu
                    if accessible:
                        liste_positions_accessibles.append([i,j])
                        liste_successeurs.append(othellier_local)

                j += 1
            i +=1
        
        return liste_positions_accessibles, liste_successeurs



class Arbre(object):
    
    def __init__(self, othellier_racine, couleur):
        self.profondeur = 0 # profondeur de l'arbre
        self.othellier_racine = othellier_racine # othellier racine
        self.dico_global = {"othellier_0" : self.othellier_racine} # Attribut TRES important --> clef = nom othellier, et valeur = 1 instance de Othellier.
                                                                    # c'est dedans qu'on construit tout l'arbre.
        # self.joueurMax = joueurMax # True si le joueur Max joue au niveau 0
        self.couleur = couleur # couleur jouée au 1er coup (après othellier racine) important pour pouvoir appeler la fonction successeur
    
    def __str__(self):
        return str(self.othellier_racine)

    # Méthode qui construit l'arbre de l'othellier racine jusqu'à la profondeur choisie
    # Entrées : self. Et nécessite attributs couleur (pour méthode successeur), profondeur.
    # Uttilise la méthode .successeurs() de la classe Othellier qui retourne 2 listes dont la liste de tous les successeurs (objets) d'un othellier donné.
    # Action : stocke dans dico_global tous les othelliers de chaque niveau, et stocke pour chaque othellier la liste des noms de ses successeurs
    # Problème rencontré : si arbre peut pas construire jusqu'à profondeur demandée parce qu'il rencontre un othellier terminal avant, il doit s'arrêter et maj sa profondeur réelle
    def construire(self, prof_max, niveau_depart_exploration, couleur):
        
        # On part du max(niveau_depart_exploration, profondeur)
        prof = max(niveau_depart_exploration,self.profondeur)+1 # la 1ère profondeur à construire est celle juste après le max
        existe_othellier_terminal = False

        # On initialiste la liste des noms des othelliers à développer sur la 1ère itération
        liste_prof_i = [clef for clef in self.dico_global.keys() if clef.split("_")[1] == str(prof-1)]
        liste_prof_i_plus_1 = []

        while (prof <= prof_max): # va de prof à prof_max-1 , sauf si rencontre othellier terminal = arrêt
            compteur = 0
            # Pour chaque othellier du niveau i (othellier = le nom string)
            for othellier in liste_prof_i:
                liste_successeurs_locale = []

                # Si 1 othellier n'a pas de successeur, il faut arrêter de construire l'arbre
                if self.dico_global[othellier].successeurs(couleur)[1] == []:
                    self.profondeur = prof-1 # très important de maj la profondeur réelle de l'arbre
                    existe_othellier_terminal = True
                    # Et supprimer tous les othelliers successeurs déjà créés pour la profondeur prof

                    for clef in list(self.dico_global.keys()):
                        if   clef.split("_")[1] == str(self.profondeur):
                            del self.dico_global[clef]
                    break
                
                if existe_othellier_terminal:
                    break

                # pour chaque successeur de l'othellier (au sens objet)
                for successeur in self.dico_global[othellier].successeurs(couleur)[1]:
                    compteur += 1
                    self.dico_global["othellier_"+str(prof)+"_"+str(compteur)] = successeur
                    liste_prof_i_plus_1.append("othellier_"+str(prof)+"_"+str(compteur))
                    liste_successeurs_locale.append("othellier_"+str(prof)+"_"+str(compteur))
                
                self.dico_global[othellier].liste_successeurs = liste_successeurs_locale.copy() # pour chaque othellier, on stocke le NOM de ses successeurs
            

            liste_prof_i = liste_prof_i_plus_1.copy() # nouvelle liste à parcourir pour le niveau suivant
            liste_prof_i_plus_1 = []

            prof += 1
        
        # S'il n'y a pas eu d'othellier terminal, alors on est bien allé jusqu'à la profondeur maximale
        if not existe_othellier_terminal:
            self.profondeur = prof_max
    # MAJ la profondeur de l'arbre (attribut) à la fin

        # print("dico",self.dico_global)

    
    def afficher(self):
        for clef, othellier in self.dico_global.items():
            print(clef, " : ")
            othellier.afficher()


    # Méthode qui applique l'algorithme min_max à l'arbre construit
    # Entrée : self, mais utilise : profondeur
    # Sortie : othellier cible = successeur de l'othellier racine à choisir
    def min_max(self, fonction_evaluation, niveau_depart_exploration, couleur):
        # On construit la listes des noms des othelliers terminaux
        liste_feuilles = [clef for clef in self.dico_global.keys() if clef.split("_")[1] == str(self.profondeur)]
        # On calcule la fonction d'évaluation pour chaque feuille
        for othellier in liste_feuilles:
            self.dico_global[othellier].score = fonction_evaluation(self.dico_global[othellier],couleur)

        print("niveau dep explo +1 :",niveau_depart_exploration+1)
        print("self.prof", self.profondeur)
        # On remonte niveau par niveau depuis les feuilles jusqu'à niveau_depart_exploration
        for prof in reversed(range(niveau_depart_exploration+1,self.profondeur)): # va de self.profondeur-1 à niveau_depart_exploration+1 -->  ne pas mettre niveau_depart_exploration+1 car sert à R et comme ça on récupère liste_othelliers_parents après la boucle et on prend le max dedans
            # Liste des noms des othelliers parents à cette profondeur
            liste_othelliers_parents = [clef for clef in self.dico_global.keys() if clef.split("_")[1] == str(prof)]
            #print("prof ",prof, liste_othelliers_parents)

            # Distinction de 2 cas selon si c'est au tour de Max ou Min de jouer
            # Vu que Max commence toujours à l'othellier racine, on regarde juste si la profondeur est mutliple de 2 pour savoir si on fait max ou min
            if (prof-niveau_depart_exploration) % 2 == 0 :
                for othellier_parent in liste_othelliers_parents: # Pour chaque othellier parent, on calcule max(successeurs)
                    scores_successeurs = [self.dico_global[successeur].score for successeur in self.dico_global[othellier_parent].liste_successeurs] 
                    self.dico_global[othellier_parent].score = max(scores_successeurs)
            else:
                for othellier_parent in liste_othelliers_parents: # Pour chaque othellier parent, on calcule min(successeurs)
                    scores_successeurs = [self.dico_global[successeur].score for successeur in self.dico_global[othellier_parent].liste_successeurs] 
                    self.dico_global[othellier_parent].score = min(scores_successeurs)
            
        # On choisit l'othellier cible = 1er coup à jouer
        scores_niveau_exploration_plus_1 = [self.dico_global[othellier].score for othellier in liste_othelliers_parents]
        othellier_cible = liste_othelliers_parents[scores_niveau_exploration_plus_1.index(max(scores_niveau_exploration_plus_1))]
        # othellier_cible est le nom de l'othellier joué au niveau niveau_depart_exploration + 1

        # On supprimme tous les autres othelliers du niveau niveau_depart_exploration + 1, ainsi que tous leurs successeurs
        othelliers_a_supprimer = [clef for clef in self.dico_global.keys() if (clef.split("_")[1] == str(niveau_depart_exploration+1)) and clef != othellier_cible]
        othelliers_parents = othelliers_a_supprimer.copy()

        for prof in range(niveau_depart_exploration+1,self.profondeur):
            liste_successeurs = []
            for othellier in othelliers_parents:
                for successeur in self.dico_global[othellier].liste_successeurs:
                    liste_successeurs.append(successeur)
                    othelliers_a_supprimer.append(successeur)
            othelliers_parents = liste_successeurs.copy()

        for clef in othelliers_a_supprimer:
            self.dico_global.pop(clef, None)

        # On retourne l'othellier cible à choisir depuis le niveau niveau_depart_exploration
        return self.dico_global[othellier_cible]

    # Que pasa si 2 successeurs ont le même score ?


class MachineVsMachine(object):
    '''
    Classe permettant de lancer 1 partie Machine VS Machine. On les appelle Blanc et Noir. On impose que la première machine à jouer est Blanc.
    On n'impose pas d'othellier racine classique (2 noirs, 2 blancs), car dans MCTS je pense qu'on voudra lancer des parties à partir d'un othellier racine qui n'est pas l'othellier de départ classique.
    Blanc et Noir jouent à tour de rôle jusqu'à que la fin de partie soit déclenchée.
    '''
    def __init__(self, othellier_racine, param_blanc, param_noir):
        self.othellier_racine = othellier_racine
        self.param_blanc = param_blanc # liste des paramètres de M1 [prof,algo, fonction évaluation ] --> bien définir l'ordre et ce qu'il y a dedans
        self.param_noir = param_noir # liste des paramètres de M2 [prof, algo, fonction évaluation ]
        self.liste_othelliers = []
        self.gagnant = ""
    
    # Méthode d'instance qui réalise les tours de la partie
    # Entrée : param_noir, param_blanc
    # Action : elle met en attribut de l'instance la liste des othelliers successifs de la partie + le joueur gagnant
    def jouer(self):

        couleur_tour_i = "blanc" # M1 commence et il est blanc
        param_tour_i = self.param_blanc
        niveau_depart_exploration = 0 # d'où on part pour construire l'arbre

        liste_othelliers = [self.othellier_racine] # objets
        arbre = Arbre(self.othellier_racine, couleur = "blanc")

        continuer_jouer = True
        # On enchaine les tours jusqu'à ce qu'on déclenche une fin de partie
        while continuer_jouer:
            
            # print("taille liste : ",len(liste_othelliers))
            # print(" joueur : ", couleur_tour_i)
            liste_othelliers[-1].afficher()

            if liste_othelliers[-1].successeurs(couleur_tour_i)[1] == []:
                continuer_jouer = False

            else:
                prof_max = niveau_depart_exploration + param_tour_i[0] # départ + profondeur d'exploration

                # On construit l'arbre pour ce tour
                arbre.construire(prof_max, niveau_depart_exploration, couleur_tour_i)
                # On récupère l'othellier à jouer et on supprimes le sous-arbre qu'on exclut en choisissant l'othellier cible
                liste_othelliers.append(arbre.min_max(param_tour_i[1],niveau_depart_exploration,couleur_tour_i))
            
                # A chaque fin de tour, on change de joueur
                if couleur_tour_i == "blanc":
                    couleur_tour_i = "noir"
                    param_tour_i = self.param_noir
                else:
                    couleur_tour_i = "blanc"
                    param_tour_i = self.param_blanc
                
                # Quand on change de tour, on avance d'un niveau dans l'arbre = on a choisi l'othellier du niveau n+1
                niveau_depart_exploration += 1
        
        # Quand partie finie, on regarde qui gagne sur le dernier othellier.
        if self.liste_othelliers[-1].gagnant() == "blanc":
            self.gagnant = "blanc"
        else:
            self.gagnant = "noir"





# Initialisation d'un othellier
tablier_0 = np.array([[Case("vide") for i in range (8)] for j in range (8)])
tablier_0[3,3] = Case("blanc")
tablier_0[4,4] = Case("blanc")
tablier_0[3,4] = Case("noir")
tablier_0[4,3] = Case("noir")
othellier_0 = Othellier(tablier_0)
# print("othellier départ :")
# othellier_0.afficher()




# # Tests fonction successeurs()
# print(othellier_0.successeurs("blanc")[0]) # on a bien la liste des positions accessibles
# # print(othellier_0.successeurs("blanc")[1]) # on a bien la liste des othelliers successeurs

# # Test construction d'un arbre
# arbre = Arbre(othellier_0, profondeur = 5, joueurMax = False, couleur = "blanc") # paramètres importants
# arbre.construire()
# # arbre.afficher() # on a bien construit l'arbre avec pour chaque othellier ses successeurs au niveau suivant, et on alterne bien blanc/noir
# # print(arbre.dico_global["othellier_1_4"].liste_successeurs) # on a bien stocké pour chaque othellier de l'arbre ses successeurs, sauf pour les feuilles
# print(arbre.dico_global.keys())

# # Test min/max
# othellier_cible = arbre.min_max(hasard)
# print(othellier_cible, " : ")
# arbre.dico_global[othellier_cible].afficher()

# Test de lancement de plusieurs parties
# Idée du test = on fait faire l'algo min max à Blanc avec la fonc d'éval evaluate_corner
# et Noir joue au hasard --> on regarde si blanc gagne plus ou pas.
nb_partie = 10
param_blanc_0 = [3, evaluate_corner] # profondeur et fonction d'évaluation utilisée
param_noir_0 = [3, hasard]

partie_0 = MachineVsMachine(othellier_0, param_blanc = param_blanc_0, param_noir = param_noir_0)
partie_0.jouer()
print(partie_0.gagnant)








