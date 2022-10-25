## IMPORTATIONS PREALABLES
import ssl
import numpy as np
from math import *
from tkinter import *
import tkinter as tk
from random import randint, random
import copy as copy
# from PIL import ImageTk, Image


## Définition des classes

class Case(object):

    def __init__(self, statut = "vide"):
        self.statut = statut
    
    # Méthode mettant à jour le statut des cases quand un coup est joué
    def maj_statut(self, couleur = "blanc", ):
        pass

    def __str__(self):
        return str(self.statut)


class Othellier(object):

    def __init__(self, tablier = 0):
        self.tablier = tablier # matrice 8x8 contenant les Cases
        self.liste_successeurs = []
        self.score = 0 # valeur de la fonction d'évaluation ou max/min des successeurs
        # self.joueur = joueur # "blanc" si c'est au joueur blanc de jouer, "noir" sinon

    # A garder pour quand on aura les cases dans le tablier --> ça affiche une matrice de statuts
    # def __str__(self):
    #     matrice_affichage = np.array([[self.tablier[i,j].statut for i in range (8)] for j in range (8)])
    #     return str(matrice_affichage)
    def __str__(self):
        return str(self.tablier[0,0])


    # Calcule le score de l'othellier
    def calcul_score(self, fonction_evaluation):
        if self.terminal:
            self.score = fonction_evaluation(self)
        elif self.joueur == "blanc":
            pass
    
    # Calcule le nombre de coups possibles pour le joueur "blanc"
    def nombre_successeurs(self):
        pass

    # Cette méthode retourne les positions où le joueur peut jouer
    # Entrée : 1 othellier
    # Sortie : liste de couples positions dans la matrice
    def positions_successeurs(self):
        pass

    # Entrée : othellier, position où on joue
    # Modifie les couleurs de l'othellier selon le coup joué
    # Sortie : nouvel othellier
    # On s'en servira pour avancer quand décision prise + quand on veeut faire les simulations
    # Remplace fonction successeurs()
    def jouer():
        pass

    # Retourne la LISTE des othelliers successeurs
    # Ajouter boucle comprehension avec position_successeurs et jouer au début de méthode construction à la place de ça
    def successeurs(self):
        return [Othellier(self.tablier+1),Othellier(self.tablier+2)]
    


class Arbre(object):
    
    def __init__(self, othellier_racine, profondeur = 5):
        self.profondeur = profondeur # profondeur de l'arbre
        self.othellier_racine = othellier_racine # othellier racine
        self.dico_global = {"othellier_0" : self.othellier_racine} # Attribut TRES important --> clef = nom othellier, et valeur = 1 instance de Othellier.
                                                                    # c'est dedans qu'on construit tout l'arbre. 
    
    def __str__(self):
        return str(self.othellier_racine)

    # Méthode qui construit l'arbre de l'othellier racine jusqu'à la profondeur choisie
    # Elle utilise la méthode .successeurs() de la classe Othellier qui retourne une liste de tous les successeurs possibles d'un othellier donné.
    def construction(self):
        #self.dico_global["othellier_1"] = self.othellier_racine.successeurs()
        #liste_prof_i = self.othellier_racine.successeurs()
        liste_prof_i = ["othellier_0"] # Liste des NOMS des othelliers
        liste_prof_i_plus_1 = []

        for prof in range(1,self.profondeur+1):
            compteur = 0
            for othellier in liste_prof_i: # Pour chaque othellier du niveau i (othellier = le nom string)
                liste_successeurs_locale = []
                for successeur in self.dico_global[othellier].successeurs(): # pour chaque successeur de l'othellier (au sens objet)
                    compteur += 1
                    self.dico_global["othellier_"+str(prof)+"_"+str(compteur)] = successeur
                    liste_prof_i_plus_1.append("othellier_"+str(prof)+"_"+str(compteur))
                    liste_successeurs_locale.append("othellier_"+str(prof)+"_"+str(compteur))
                
                self.dico_global[othellier].liste_successeurs = liste_successeurs_locale.copy() # pour chaque othellier, on stocke le NOM de ses successeurs
            
            liste_prof_i = liste_prof_i_plus_1.copy() # nouvelle liste à parcourir pour le niveau suivant
            liste_prof_i_plus_1 = []

        # A la fin, on remplace dans dico les valeurs (objet) par leur tablier pour pouvoir mieux voir ce qu'il se passe
        # A SUPPRIMEER A LA FIN
        for clef, othellier in self.dico_global.items():
            self.dico_global[clef] = othellier.tablier[0,0]
    
    # Méthode qui applique l'algorithme min_max à l'arbre construit
    def min_max(self):
        
        liste_feuilles = [clef for clef in self.dico_global.keys() if clef.split("_")[1] == str(self.profondeur)] # liste des noms des othelliers au niveau feuille
        print(liste_feuilles)
        # On calcule la fonction d'évaluation pour chaque feuille
        for othellier in liste_feuilles:
            self.dico_global[othellier].score = fonction_evaluation(self.dico_global[othellier])
            pass
        
        # On remonte niveau par niveau jusqu'à la racine
        for prof in reversed(range(1,self.profondeur)): # va de profondeur-1 à 1
            pass
        # 1 difficulté = savoir si J1 ou J2 joue

            




# Construction d'un arbre
profondeur = 5
tablier = np.zeros((8,8))

othellier_0 = Othellier(tablier)
arbre = Arbre(othellier_0, profondeur)
arbre.construction()
print(arbre.dico_global)
#arbre.min_max()


















