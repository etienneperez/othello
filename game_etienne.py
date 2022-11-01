import profile
import ssl
import numpy as np
from math import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from random import randint, random
import copy as copy

import fonction_annexe as fct

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


    # Méthode pour afficher un othellier.
    def afficher(self):
        couleur = ""
        for i in range(8):
            for j in range(8):
                if self.tablier[i,j] == 1:
                    couleur = "white"
                elif self.tablier[i,j] == -1:
                    couleur = "black"
                else:
                    couleur = "green"
                canvas2.create_rectangle(10+i*long, 10+j*long, 10+(i+1)*long, 10+(j+1)*long, fill = "green")
                canvas2.create_oval(10+i*long +long/7, 10+j*long +long/7, 10+(i+1)*long -long/7, 10+(j+1)*long -long/7, fill = couleur, outline = "green")
                j += 1
            i += 1


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
    
  
class Partie(object):

    def __init__(self,Display = True,list_IAtype = ['MinMax','MinMax'], list_prof = [3,3], list_MCTS_N = [50,50],list_MCTS_T = [3,3],list_MCTS_C = [2,2]):
        self.liste_othellier = [] #liste des othelliers jouées
        self.tour_nb = 0 #à quel tour est-on
        self.joueurs = ["Joueurs : "] #liste de deux instances joueurs
        self.tour_joueur = 1 #Numéro du joueur qui doit jouer au tour actuel
        self.Display = Display #True si on veut un affichage visuel de la partie, False si on veut uniquement le résultat de la partie
                                # Si on joue sans affichage, on joue forcément sans IA
        #Ces trois attributs servent uniquement si on joue sans affichage, ils définissent les IA qui s'affrontent dans ce cas là
        #Ce sont des listes de tailles deux : un élément pour chaque joueur
        self.list_IAtype = list_IAtype #Type de l'IA Minmax, AlphaBeta, MCTS
        self.list_prof = list_prof #Prof
        self.list_MCTS_N = list_MCTS_N  #Nombre de simulations pour le MCTS
        self.list_MCTS_T = list_MCTS_T  #Nombre de simulations pour le T de l'algo MCTS
        self.list_MCTS_C = list_MCTS_C  #Nombre de simulations pour le S de l'algo MCTS

        self.result = 0 #Résultat de la partie 
        self.player1prof = list_prof[0] #prof max du joueur 1, nécessaire pour la création de l'othellier initial
        self.ask_define_player() #création des deux joueurs
        self.init_othellier() #initialisation de l'othellier 
        if self.Display : #si on a un affichage
            global fenetre2, canvas2
            fenetre2 = tk.Tk()
            fenetre2.configure(height = 20*long, width = 20*long)
            canvas2 = tk.Canvas(fenetre2, width=10*long, height=10*long, background='white')
            canvas2.pack()
            # On fait tourner le jeu qui affiche les othelliers au fur et à mesure
            self.game_with_display() #Jeu

            fenetre2.mainloop()
        else : 
            self.game() #Jeu
            

    
    def init_othellier(self): 
        #Création de l'othellier initial
        tablier_0 = np.array([[0 for i in range (8)] for j in range (8)])
        tablier_0[3,3] = 1
        tablier_0[4,4] = 1
        tablier_0[3,4] = -1
        tablier_0[4,3] = -1
        #On commence par le joueur 1, c'est arbitraire
        #Initialisation de liste retenant les othelliers joués (peut-être un peu lourd de tous les retenir, en soit il suffit d'en retenir un seul donc on pourra changer)
        self.liste_othellier = [Othellier(self.player1prof,1,tablier_0)]

    def ask_define_player(self):
        #Demande à l'utilisateur de rentrer le type de joueurs qu'il veut voir s'affronter 
        #Possibilités : utilisateur ou IA
        #Si IA : MCTS, MinMax ou AlphaBeta et indiquer la profondeur d'exploration
        #self.joueurs.append(joueur1) sachant que joueur1 = Joueur(1,True/False,IAtype,prof,prof_adv,nb_simul_MCTS)
        #self.joueurs.append(joueur2) sachant que joueur2 = Joueur(-1,True/False,IAtype,prof,prof_adv,nb_simul_MCTS)
        # + il faut modifier self.player1prof pour pouvoir créer l'othellier initial

        if self.Display :
            global long
            long = 80

            fenetre = tk.Tk() # crée une fenêter sur laquelle on va pouvoir travailler
            fenetre.configure(height = 20*long, width = 20*long) # Règle les paramètres de la fenêtre --> laisse une marge de 3*long autour du tablier

            canvas = tk.Canvas(fenetre, width=10*long, height=10*long, background='white')

            label = tk.Label(fenetre, text="Qui voulez-vous voir jouer ? Avec quels paramètres ?", font=("Helvetica", 20))
            label.place(x = 10 + 4*long, y = 10 + long)

            type_joueur = ["humain","machine"]
            type_1 = StringVar()
            label = tk.Label(fenetre, text="Joueur 1", font=("Helvetica", 20))
            label.place(x = 10 + 5*long, y = 10 + 2*long)
            widget = ttk.Combobox(fenetre, textvariable = type_1, values=type_joueur)
            widget.current(1)
            widget['state'] = 'readonly'
            widget.place(x = 10 + 4*long, y= 3*long)
            type_2 = StringVar()
            label = tk.Label(fenetre, text="Joueur 2", font=("Helvetica", 20))
            label.place(x = 10 + 8*long, y = 10 + 2*long)
            widget = ttk.Combobox(fenetre, textvariable = type_2, values=type_joueur)
            widget.current(1)
            widget['state'] = 'readonly'
            widget.place(x = 10 + 7*long, y= 3*long)
            

            IAtype = ["MinMax","AlphaBeta","MCTS"]
            IAtype_1 = StringVar()
            label = tk.Label(fenetre, text="Quel algorithme ?", font=("Helvetica", 16))
            label.place(x = 10 + 2*long, y = 4*long)
            widget = ttk.Combobox(fenetre, textvariable = IAtype_1, values=IAtype)
            widget.current(0)
            widget['state'] = 'readonly'
            widget.place(x = 10 + 4*long, y= 4*long)
            IAtype_2 = StringVar()
            widget = ttk.Combobox(fenetre, textvariable = IAtype_2, values=IAtype)
            widget.current(0)
            widget['state'] = 'readonly'
            widget.place(x = 10 + 7*long, y= 4*long)
            

            label = tk.Label(fenetre, text="Quelle profondeur d'exploration ?", font=("Helvetica", 16))
            label.place(x = 10 + long, y = 5*long)
            prof_1 = tk.IntVar()
            prof_1.set(3)
            widget = tk.Scale(fenetre, variable=prof_1, orient='horizontal', from_=1, to=6, resolution=1, tickinterval=1, length=100)
            widget.place(x = 10 + 5*long, y = 5*long)
            prof_2 = tk.IntVar()
            prof_2.set(3)
            widget = tk.Scale(fenetre, variable=prof_2, orient='horizontal', from_=1, to=6, resolution=1, tickinterval=1, length=100)
            widget.place(x = 10 + 8*long, y = 5*long)
            
            
            label = tk.Label(fenetre, text="MCTS : nombre de simulations ?", font=("Helvetica", 16))
            label.place(x = 10 + long, y = 6*long)
            MCTS_N_1 = tk.IntVar()
            MCTS_N_1.set(10)
            widget = tk.Scale(fenetre, variable=MCTS_N_1, orient='horizontal', from_=1, to=100, resolution=1, tickinterval=25, length=100)
            widget.place(x = 10 + 5*long, y = 6*long)
            MCTS_N_2 = tk.IntVar()
            MCTS_N_2.set(10)
            widget = tk.Scale(fenetre, variable=MCTS_N_2, orient='horizontal', from_=1, to=100, resolution=1, tickinterval=25, length=100)
            widget.place(x = 10 + 8*long, y = 6*long)
            

            label = tk.Label(fenetre, text="MCTS : T ?", font=("Helvetica", 16))
            label.place(x = 10 + long, y = 7*long)
            MCTS_T_1 = tk.IntVar()
            MCTS_T_1.set(5)
            widget = tk.Scale(fenetre, variable=MCTS_T_1, orient='horizontal', from_=1, to=5, resolution=1, tickinterval=1, length=100)
            widget.place(x = 10 + 5*long, y = 7*long)
            MCTS_T_2 = tk.IntVar()
            MCTS_T_2.set(5)
            widget = tk.Scale(fenetre, variable=MCTS_T_2, orient='horizontal', from_=1, to=5, resolution=1, tickinterval=1, length=100)
            widget.place(x = 10 + 8*long, y = 7*long)
            

            label = tk.Label(fenetre, text="MCTS : paramètre C ?", font=("Helvetica", 16))
            label.place(x = 10 + long, y = 8*long)
            MCTS_C_1 = tk.IntVar()
            MCTS_C_1.set(2)
            widget = tk.Scale(fenetre, variable=MCTS_C_1, orient='horizontal', from_=1, to=5, resolution=1, tickinterval=1, length=100)
            widget.place(x = 10 + 5*long, y = 8*long)
            MCTS_C_2 = tk.IntVar()
            MCTS_C_2.set(2)
            widget = tk.Scale(fenetre, variable=MCTS_C_2, orient='horizontal', from_=1, to=5, resolution=1, tickinterval=1, length=100)
            widget.place(x = 10 + 8*long, y = 8*long)
            
            bouton = tk.Button(fenetre, text="Valider et lancer la partie", command = fenetre.destroy)
            bouton.place(x = 7*long, y= 9*long)

            canvas.pack()
            fenetre.mainloop()

            type_joueur_1 = type_1.get()
            type_joueur_2 = type_2.get()
            IAtype_joueur_1 = IAtype_1.get()
            IAtype_joueur_2 = IAtype_2.get()
            prof_joueur_1 = prof_1.get()
            prof_joueur_2 = prof_2.get()
            MCTS_N_joueur_1 = MCTS_N_1.get()
            MCTS_N_joueur_2 = MCTS_N_2.get()
            MCTS_T_joueur_1 = MCTS_T_1.get()
            MCTS_T_joueur_2 = MCTS_T_2.get()
            MCTS_C_joueur_1 = MCTS_C_1.get()
            MCTS_C_joueur_2 = MCTS_C_2.get()

            # print("type_joueur_1",type_joueur_1)
            # print("type_joueur_2",type_joueur_2)
            # print("IAtype_joueur_1",IAtype_joueur_1)
            # print("IAtype_joueur_2",IAtype_joueur_2)
            # print("prof_joueur_1",prof_joueur_1)
            # print("MCTS_C_joueur_1", MCTS_C_joueur_1)
            joueur1 = Joueur(1, IA = (type_joueur_1 == "machine"),IAtype = IAtype_joueur_1, prof = prof_joueur_1, prof_adv = prof_joueur_2, MCTS_N = MCTS_N_joueur_1, MCTS_T = MCTS_T_joueur_1, MCTS_C = MCTS_C_joueur_1)
            joueur2 = Joueur(-1, IA = (type_joueur_2 == "machine"),IAtype = IAtype_joueur_2, prof = prof_joueur_2, prof_adv = prof_joueur_1, MCTS_N = MCTS_N_joueur_2, MCTS_T = MCTS_T_joueur_2, MCTS_C = MCTS_C_joueur_2)

            self.list_prof = [prof_joueur_1,prof_joueur_2]
            self.player1prof = self.list_prof[0]

            self.joueurs.append(joueur1)
            self.joueurs.append(joueur2)

        #Si il n'y a pas d'affichage, les informations sur les deux joueurs sont directement dans la création de l'instance partie grace aux attribut list_IAtype, list_prof et list_nb_simul_MCTS
        else : 
            self.joueurs.append(Joueur(1,True,self.list_IAtype[0],self.list_prof[0],self.list_prof[1],self.list_MCTS_N[0],self.list_MCTS_T[0],self.list_MCTS_C[0]))
            self.joueurs.append(Joueur(-1,True,self.list_IAtype[1],self.list_prof[1],self.list_prof[0],self.list_MCTS_N[1],self.list_MCTS_T[1],self.list_MCTS_C[1]))

    # def fermer_fenetre(self):
    #     fenetre.destroy()

    def init_display(self):
        #Méthode initialisant l'affiche du plateau 
        pass

    def change_display(self):
        #Methode mettant a jour l'affichage du plateau pour qu'il corresponde à self.liste_othellier[-1]
        #Peut-être utiliser self.liste_othellier[-1].liste_coord_successeurs pour afficher les cases jouables en une couleur un peu différente
        pass

    
    def final_display(self):
        #Méthode affichant quelque chose de spécial pour la fin de partie
        #C'est pas obligatoire mais ça peut être pas mal d'avoir un affichage genre "Joueur 1 à gagné"
        
        # On affiche l'othellier final
        canvas2.delete("all")
        self.liste_othellier[-1].afficher() 

        # Et un message
        canvas2.create_rectangle(10+2.5*long, 10+2.5*long, 10+6.5*long, 10+6.5*long, fill = "red",alpha = 0.5)

        if self.liste_othellier[-1].gagnant == 1:
            gagnant = "blanc"
        elif self.liste_othellier[-1].gagnant == -1:
            gagnant = "noir"
        else:
            gagnant = "egalite"
        
        if (gagnant == "blanc") and (gagnant == "noir"):
            canvas2.create_text(10+4*long, 10+4*long, text="Le joueur {} a gagné !".format(gagnant), fill="white")
        else:
            canvas2.create_text(10+4*long, 10+4*long, text="Egalité !", fill="white")
    

    def game(self): 
        #boucle de jeu 
        while self.liste_othellier[-1].gagnant == 0 : #Si l'othellier est gagnant on s'arrête
            self.liste_othellier.append(self.joueurs[self.tour_joueur].jouer(self.liste_othellier[-1]))
            print("nouveau tour")
            # if self.Display :
            #     self.change_display()
            # print(self.liste_othellier[-1].tablier)
            self.tour_joueur = - self.tour_joueur #changement de joueur
            self.tour_nb += 1
        #Si on est en mode sans affichage, on veut juste retourner le joueur gagnant
        self.result = self.liste_othellier[-1].gagnant

    def game_with_display(self): 

        print("nouveau tour", self.tour_nb)
        print("self.tour_joueur",self.tour_joueur)
        print("self.liste_othellier[-1].gagnant",self.liste_othellier[-1].gagnant)

        # On ajoute le nouvel othellier
        self.liste_othellier.append(self.joueurs[self.tour_joueur].jouer(self.liste_othellier[-1]))

        # On affiche le nouvel othellier
        canvas2.delete("all")
        self.liste_othellier[-1].afficher()

        # On met à jour le joueur et le num du tour
        self.tour_joueur = - self.tour_joueur 
        self.tour_nb += 1

        if self.liste_othellier[-1].gagnant == 0 :
            fenetre2.after(1500,self.game_with_display)
        else:
            self.result = self.liste_othellier[-1].gagnant # on ne doit le faire que quand la partie est finie on est ok ?
            print("fin partie au tour",self.tour_nb)
            fenetre2.after(1500,self.final_display)

        


class Joueur(object):

    def __init__(self,nb_joueur = 1,IA = True,IAtype = 'MinMax', prof = 1,prof_adv = 1,MCTS_N =50,MCTS_T = 3,MCTS_C = 2):
        self.nb_joueur = nb_joueur #Joueur 1 ou joueur -1
        self.IA = IA #Boléen pour savoir si c'est un joueur IA (true) ou un vrai joueur (false)
        self.IAtype = IAtype #Si c'est un IA, quel type d'IA : MinMax, AlphaBeta, MCTS (MinMax par défaut)
        self.prof = prof #Si c'est un IA, la profondeur d'exploration (3 par défaut)
        self.prof_adv = prof_adv
        self.MCTS_N = MCTS_N #Si c'est un IA MCTS, le nombre de simulation (50 par défaut)
        self.MCTS_T = MCTS_T
        self.MCTS_C = MCTS_C


    #Méthode prenant en entrée un othellier et donnant en sortant l'othellier une fois que le joueur a joué 
    def jouer(self,othellier):
    #Selon les types de joueurs, on appelle differentes fonctions de choix du move à faire
        if self.IA : 
            if self.IAtype == 'MinMax' : 
                return self.compMoveMinMax(othellier)
            if self.IAtype == 'AlphaBeta' : 
                return self.compMoveAlphaBeta(othellier)
            if self.IAtype == 'MCTS' : 
                return self.compMoveMCTS(othellier)
        else : 
            return self.joueurMove(othellier)

    #Prend en entrée un othellier, la profondeur max d'exploration et le joueur qui joue 
    #En sortie : le tablier resultant du move qu'il a fait
    def compMoveMinMax(self,othellier):

        # Pour gérer le cas où il n'y a qu'1 seul successeur possible on le joue direct
        # Gère aussi le cas où celui d'avant a precedent_passe = True --> la partie va se finir car il a gagnant = 1 ou -1
        if len(othellier.liste_successeurs) == 1:
            return Othellier (self.prof_adv,-self.nb_joueur,othellier.liste_successeurs[0].tablier,othellier.liste_successeurs[0].precedent_passe)

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
            score = fct.MinMax(son,self.prof-1,-self.nb_joueur,False)
            # print("score",score)
            #Ici, on cherche à maximiser le score du joueur, donc si le score dépasse le score max jusqu'à là :  
            # On change le best score et on retient le tablier du successeurs qui a ce nouveau score max
            if score > bestScore : 
                bestScore = score
                bestMove = son.tablier
                ppasse = son.precedent_passe
        # Idée = on a la double info de ppasse et de prof.
        # Car si on retourne un successeur, perd de la prof au fur et à mesure des tours
        return Othellier(self.prof_adv,-self.nb_joueur,bestMove,ppasse)


    def compMoveAlphaBeta(self,othellier):

        # Pour gérer le cas où il n'y a qu'1 seul successeur possible on le joue direct
        # Gère aussi le cas où celui d'avant a precedent_passe = True --> la partie va se finir car il a gagnant = 1 ou -1
        if len(othellier.liste_successeurs) == 1:
            return Othellier (self.prof_adv,-self.nb_joueur,othellier.liste_successeurs[0].tablier,othellier.liste_successeurs[0].precedent_passe)

        # Pour gérer le cas où prof = 1 --> on retourne juste le max des successeurs
        if self.prof == 1:
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
            return Othellier(self.prof_adv,-self.nb_joueur,bestMove,ppasse)

        # Initialisation de alpha et beta
        alpha = -100000000
        beta = 100000000
        ppasse = False
        # On lance alpha-beta qui retourne le score de l'othellier cible vers lequel on doit aller
        score_alpha_beta = fct.AlphaBeta(othellier,self.prof,self.nb_joueur,alpha,beta,True)
        # On détermine quel othellier jouer pour être sur la branche qui mène à l'othellier cible dont le score est score_alpha_beta
        for othellier_a_jouer in othellier.liste_successeurs:
            liste_successeurs_prof_i = othellier_a_jouer.liste_successeurs
        
            for i in range(1,self.prof): # il faut faire prof-2 fois la boucle en gros, sinon après on atteint les feuilles et le calcul des successeurs fait une erreur. Donc 
                                # donc on fait prof-1 fois la boucle et on met une condition sur le calcul des successeurs.
                liste_successeurs_prof_i_plus_1 = []
                for successeur in liste_successeurs_prof_i:
                    if successeur.score == score_alpha_beta:
                        return Othellier(self.prof,-self.nb_joueur,othellier_a_jouer.tablier,othellier_a_jouer.precedent_passe)
                    if i < self.prof-1: # cf explication plus haut, pour la dernière profondeur, one ne veut pas calculer les successeurs
                        for successeur_de_successeur in successeur.liste_successeurs:
                            liste_successeurs_prof_i_plus_1.append(successeur_de_successeur)
                liste_successeurs_prof_i = liste_successeurs_prof_i_plus_1.copy()

    def compMoveMCTS(self,othellier):

        #On initialise le score max à une valeur très basse
        bestScore = -10000
        #On initialise le tablier de sortie comme on veut
        bestMove = np.array([[0 for i in range (8)] for j in range (8)])

        for T in range(self.MCTS_T): # on fait T fois le processus de MCTS
            fct.MCTS(othellier, self.prof, self.MCTS_C, T) #ajouter en paramétre N, nombre de simulations, MCTS_N
        
        ppasse = FALSE
        #On va parcourir les successeurs de l'othellier actuel
        #C'est un de ces successeurs que l'on va choisir, il faut donc les évaluer
        for son in othellier.liste_successeurs: 
            score = son.t
            #Ici, on cherche à maximiser le score du joueur, donc si le score dépasse le score max jusqu'à là :  
            # On change le best score et on retient le tablier du successeurs qui a ce nouveau score max
            if score > bestScore : 
                bestScore = score
                bestMove = son.tablier
                ppasse = son.precedent_passe
        return Othellier(self.prof_adv, -self.nb_joueur, bestMove, ppasse)
    

    def joueurMove(self,othellier) : 
        #Demander au joueur où il veut jouer 
        #return l'othellier modifié 
        pass

# print(Partie(Display = False,list_IAtype = ['MinMax','AlphaBeta'], list_prof = [2,3]).result)




partie_1 = Partie()







