import numpy as np
from math import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from random import randint
import copy as copy
import time


########################## Classe Othellier #####################################
class Othellier(object):

    def __init__(self, prof,joueur,tablier, passe = FALSE,isMCTS = False):
        """
        Initialise les attributs fournis en arguments et exécute la méthode successeurs()
        """
        self.prof = prof # Profondeur d’exploration de l’algorithme de jeu à partir de cet othellier
        self.joueur = joueur # Entier valant 1 si le joueur blanc joue à partir de cet othellier, et -1 si le joueur noir joue à partir de cet othellier
        self.tablier = tablier # Matrice 8x8 dont les éléments sont des entiers qui valent 0 (case vide), 1 (pion blanc) ou -1 (pion noir)
        self.liste_successeurs = [] # Liste des othelliers fils (liste d’instances de cette même classe Othellier) correspondant à chaque othellier potentiel obtenu après que le joueur a joué son pion 
        self.liste_coord_successeurs = [] # Liste des positions (dans la matrice) des othelliers fils présents dans liste_successeurs
        self.gagnant = 0 # Entier valant 0 par défaut, et si l’othellier est terminal (plus aucun joueur ne peut jouer) il vaut 1 si le joueur blanc a gagné, -1 si le joueur noir a gagné et 2 s’il y a égalité
        self.precedent_passe = passe #Booléen valant True si le joueur précédent a passé son tour et False sinon. Cela permet d’arrêter la partie si les deux joueurs passent successivement
        self.isMCTS = isMCTS
        if not isMCTS : 
            self.successeurs_bis()
        self.score = -1000000 # Réel utilisé dans l’algorithme alpha-bêta pour stocker le alpha/bêta remonté au niveau de chaque othellier
        self.t = 10000 # Nombre de parties gagnées par un othellier ou un de ses othelliers successeurs. Par défaut très élevé car peut varier entre -N*T et N*T.
        self.n = 0 # Nombre de fois qu'un othellier ou un de ses othelliers successeurs a été visité.



    def afficher(self):
        """
        Affiche l’othellier sur le canvas de la fenêtre à partir de l’attribut tablier en représentant les éléments valant 1 par un pion blanc et -1 par un pion noir.
        Entrée : Instance de la classe Othellier
        Pas de sortie
        """
        couleur = ""
        for i in range(8): 
            for j in range(8):
                texte = ""
                if self.tablier[i,j] == 1:
                    couleur = "white"
                elif self.tablier[i,j] == -1:
                    couleur = "black"
                elif [i,j] in self.liste_coord_successeurs:
                    couleur = "green"
                    texte = "accessible"
                else:
                    couleur = "green"
                canvas2.create_rectangle(10+j*long, 10+i*long, 10+(j+1)*long, 10+(i+1)*long, fill = "green")
                canvas2.create_oval(10+j*long +long/7, 10+i*long +long/7, 10+(j+1)*long -long/7, 10+(i+1)*long -long/7, fill = couleur, outline = "green")
                canvas2.create_text(10+(j+0.5)*long, 10+(i+0.5)*long, text = texte, fill = "purple", font=('Helvetica 16 bold'))
                j += 1
            i += 1

    def successeurs_bis(self): 
        """
        Génère les othelliers fils en parcourant les cases du tablier pour déterminer les positions jouables par le joueur qui joue à partir de cet othellier. 
        Cette méthode met à jour les attributs liste_successeurs et liste_coord_successeurs.
        Si aucun othellier fils n’est trouvé, elle met à jour l’attribut precedent_passe à True, et si cet attribut valait déjà True (l’othellier est terminal), elle met à jour l’attribut gagnant avec le gagnant de la partie.
        Entrée : Instance de la classe Othellier
        Pas de sortie
        """
        # Dans le cas de othellier créés dans la fonction MCTS, on ne veut que chercher les successeurs directs
        if self.isMCTS : 
            prof = 1
        else : 
            prof = self.prof

        if prof > 0 : 
            # Parcours du tablier 
            for l in range(8):
                for c in range(8):

                    #Si la case est vide
                    if self.tablier[l,c] == 0 : 

                        #Si on trouve un case vide, on ajoute un jeton dessus, ce qui donne un tablier local modifié
                        tablier_local = np.array([[0 for i in range (8)] for j in range (8)])
                        for lbis in range(8):
                            for cbis in range(8):
                                tablier_local[lbis,cbis] = self.tablier[lbis,cbis]
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
                            self.liste_successeurs.append(Othellier(self.prof-1,-self.joueur,tablier_local,isMCTS= self.isMCTS))
                        #Si la case n'était pas accessible/jouable, rien n'est ajouté aux listes successeurs
            
            # Si pas de successeurs, alors le joueur passe son tour = il joue ce même othellier et on change joueur
            if self.liste_successeurs == [] and not self.precedent_passe : 
                self.liste_successeurs = [Othellier(self.prof-1,-self.joueur,self.tablier,TRUE,isMCTS= self.isMCTS)]
            # Si pas de successeur, et que le joueur adverse avait déjà passé avant = partie finie
            if self.liste_successeurs == [] and self.precedent_passe : 
                self.isGagnant()
        else : 
            #Si on a atteint la profondeur max, on l'indique.
            self.liste_coord_successeurs = ['profmax']
            self.liste_successeurs = ['profmax']
                       
    def evaluate (self,tour_joueur):
        """
        Retourne la valeur de la fonction d’évaluation qui prend cet othellier en entrée.
        Un coin capturé vaut 60. 
        Un jeton dans le voisinage direct d'un coin non-capturé vaut -20.
        Entrée : Instance de classe Othellier, numéro du joueur à qui c'est le tour (-1 ou 1)
        Sortie : Evaluation de l'othellier
        """
        #initialisation du score
        pscore = 0
        # Parcourir les quatres coins 
        for i in [0,2]:
            for j in [0,2]:  
                ligne = int(i * 7/2)
                col = int(j * 7/2)

                # Le coin est-il capturé par le joueur dont c'est le tour
                if self.tablier[ligne,col] == tour_joueur : 
                    pscore += 100
                # Si il n'est capturé par personne   
                elif self.tablier[ligne,col] == 0 : 
                    # Est ce que le joueur dont c'est le tour a un jeton dans les cases autour du coin. 
                    if self.tablier[ligne + 1 - i,col] == tour_joueur : 
                        pscore -= 20
                    if self.tablier[ligne,col + 1 - j] == tour_joueur : 
                        pscore -= 20
                    if self.tablier[ligne + 1 - i,col + 1 - j] == tour_joueur : 
                        pscore -= 20
        return pscore

    def isGagnant(self):
        """
        Modifie l'attribut gagnant. 
        Mets 1 s’il y a une majorité de pions blancs dans le tablier, -1 s’il y a une majorité de pions noirs, et 2 sinon
        Entrée : Instance de la classe Othellier
        Pas de sortie
        """                                                        
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
    

########################## Classe Partie #####################################
class Partie(object):

    def __init__(self,Display = True,utilisateur = True,list_IAtype = ['MinMax','MinMax'], list_prof = [3,3], list_MCTS_N = [50,50],list_MCTS_T = [10,10],list_MCTS_C = [2,2]):
        """
        Crée les attributs avec les valeurs prises en argument et exécute les méthodes init_joueurs() et init_othellier(). 
        Si le mode de jeu choisi est le mode Jouer, la méthode jeu_avec_affichage est exécutée, sinon la méthode jeu_sans_affichage est exécutée.
        """
        self.liste_othellier = [] # Liste des othelliers jouées pendant la partie 
        self.tour_nb = 0 # Numéro du tour de jeu
        self.joueurs = ["Joueurs : "] # Liste des deux instances de la classe Joueur pour la partie 
        self.tour_joueur = 1 # Entier valant 1 si le joueur blanc joue à ce tour, et -1 si le joueur noir joue 
        self.Display = Display # Booléen valant True si l’utilisateur a choisi de lancer la partie en mode Jouer, 
                               # et False si l’utilisateur a lancé la partie en mode Simulation
        self.resultat = 0 # Entier initialisé à 0, et valant 1 si le joueur blanc a gagné, -1 si le joueur noir a gagné et 2 s’il y a égalité
        self.utilisateur = utilisateur 

        #Ces trois attributs servent uniquement pour nos comparaisons d'algorithmes, pas dans le cas où il n'y a pas d'utilisateur
        #Ce sont des listes de tailles deux : un élément pour chaque joueur
        self.list_IAtype = list_IAtype #Type de l'IA Minmax, AlphaBeta, MCTS
        self.list_prof = list_prof #Prof
        self.list_MCTS_N = list_MCTS_N  # Nombre de simulations totale pour le MCTS pour chaque othellier joué
        self.list_MCTS_T = list_MCTS_T  # Nombre de simulations de parties aléatoires dans le processus MCTS pour chaque othellier joué
        self.list_MCTS_C = list_MCTS_C  # Paramètre C pour le calcul de l'UCB pour chaque othellier joué

        self.init_joueurs() 
        self.init_othellier() 

        if self.utilisateur:
            if self.Display : 
                global fenetre2, canvas2
                fenetre2 = tk.Tk()
                fenetre2.configure(height = 20*long, width = 20*long)
                canvas2 = tk.Canvas(fenetre2, width=10*long, height=10*long, background='white')
                canvas2.pack()

                self.jeu_avec_affichage() #Jeu

                fenetre2.mainloop()
            else : 
                self.jeu_sans_affichage() #Jeu
        else:
            self.jeu_sans_affichage()

            
            

    
    def init_othellier(self): 
        """
        Génère l’instance correspondant à l’othellier de départ de la partie et l’ajoute à l’attribut liste_othelliers
        Entrée : Instance de la classe Partie
        Pas de sortie
        """
        tablier_0 = np.array([[0 for i in range (8)] for j in range (8)])
        tablier_0[3,3] = 1
        tablier_0[4,4] = 1
        tablier_0[3,4] = -1
        tablier_0[4,3] = -1

        #Initialisation de liste retenant les othelliers joués 
        #On commence par le joueur 1, c'est arbitraire
        self.liste_othellier = [Othellier(self.joueurs[1].prof,1,tablier_0)]

    def init_joueurs(self): 
        """
        Génère les deux instances de la classe Joueur correspondant aux joueurs choisis pour la partie et les ajoute à l’attribut joueurs. 
        Met à jour l’attribut player1prof.
        Entrée : Instance de la classe Partie
        Pas de sortie
        """
    
        if self.utilisateur :
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
            joueur1 = Joueur(1, IA = (type_joueur_1 == "machine"),IAtype = IAtype_joueur_1, prof = prof_joueur_1, prof_adv = prof_joueur_2, MCTS_N = MCTS_N_joueur_1, MCTS_T = MCTS_T_joueur_1, MCTS_C = MCTS_C_joueur_1,advisMCTS=(IAtype_joueur_2 == 'MCTS'))
            joueur2 = Joueur(-1, IA = (type_joueur_2 == "machine"),IAtype = IAtype_joueur_2, prof = prof_joueur_2, prof_adv = prof_joueur_1, MCTS_N = MCTS_N_joueur_2, MCTS_T = MCTS_T_joueur_2, MCTS_C = MCTS_C_joueur_2,advisMCTS=(IAtype_joueur_1 == 'MCTS'))

            self.joueurs.append(joueur1)
            self.joueurs.append(joueur2)            

        #Si il n'y a pas d'affichage, les informations sur les deux joueurs sont directement dans la création de l'instance partie grace aux attribut list_IAtype, list_prof et list_nb_simul_MCTS
        else : 
            self.joueurs.append(Joueur(1,True,self.list_IAtype[0],self.list_prof[0],self.list_prof[1],self.list_MCTS_N[0],self.list_MCTS_T[0],self.list_MCTS_C[0],advisMCTS=(self.list_IAtype[1] == 'MCTS')))
            self.joueurs.append(Joueur(-1,True,self.list_IAtype[1],self.list_prof[1],self.list_prof[0],self.list_MCTS_N[1],self.list_MCTS_T[1],self.list_MCTS_C[1],advisMCTS=(self.list_IAtype[0] == 'MCTS')))

    
    def afficher_gagnant(self):
        """
        Affiche le gagnant de la partie dans la fenêtre quand la partie est terminée
        Entrée : Instance de la classe Partie
        Pas de sortie
        """

        canvas2.delete("all")
        self.liste_othellier[-1].afficher() 

        canvas2.create_rectangle(10+2*long, 10+2.5*long, 10+6*long, 10+5*long, fill = "red")

        if self.liste_othellier[-1].gagnant == 1:
            gagnant = "blanc"
        elif self.liste_othellier[-1].gagnant == -1:
            gagnant = "noir"
        else:
            gagnant = "egalite"
        
        if (gagnant == "blanc") or (gagnant == "noir"):
            canvas2.create_text(10+4*long, 10+3.5*long, text="Le joueur {} a gagné !".format(gagnant), fill="white", font=("Helvetica", 25))
        else:
            canvas2.create_text(10+4*long, 10+3.5*long, text="Egalité !", fill="white",font=("Helvetica", 25))
    
    def jeu_sans_affichage(self): 
        """
        Lance une partie sans aucun affichage dans l’interface graphique : boucle qui appelle la méthode jouer() de la classe Joueur à chaque tour et ajoute l’othellier à l’attribut liste_othelliers. 
        La boucle s’arrête lorsqu’un othellier ajouté à son attribut gagnant non nul. 
        A la fin, elle met à jour l’attribut resultat. 
        Entrée : Instance de la classe Partie
        Pas de sortie
        """
        while self.liste_othellier[-1].gagnant == 0 :
            self.liste_othellier.append(self.joueurs[self.tour_joueur].jouer(self.liste_othellier[-1]))
            self.tour_joueur = - self.tour_joueur #changement de joueur
            self.tour_nb += 1
        #Si on est en mode sans affichage, on veut juste retourner le joueur gagnant
        self.resultat = self.liste_othellier[-1].gagnant


    def jeu_avec_affichage(self): 
        """
        Lance une partie en affichant l’othellier choisi à chaque tour sur l’interface graphique.
        A chaque tour : 
            Si le type de joueur est humain, la position jouée doit être choisie par un clique gauche de la souris sur le tablier.
            Si le type de joueur est machine, la méthode jouer() de la classe Joueur est appelée.
        Dans les 2 cas, l’othellier résultant du choix est ajouté à liste_othelliers à la fin du tour, et la méthode jeu_avec_affichage() est appelée à nouveau. 
        Ainsi de suite jusqu’à obtenir un othellier dont l’attribut gagnant est non nul, auquel cas la méthode afficher_gagnant() est appelée
        Entrée : Instance de la classe Partie
        Pas de sortie
        """

        # Cas où un humain joue à ce tour
        if self.joueurs[self.tour_joueur].IA == False:
            print("entrée joueur humain")

            if len(self.liste_othellier[-1].liste_successeurs) == 1:
                self.liste_othellier.append(Othellier(self.joueurs[self.tour_joueur].prof_adv,-self.tour_joueur,self.liste_othellier[-1].liste_successeurs[0].tablier,self.liste_othellier[-1].liste_successeurs[0].precedent_passe))
                
                # On affiche le nouvel othellier
                canvas2.delete("all")
                self.liste_othellier[-1].afficher()
                
                if self.liste_othellier[-1].gagnant == 0 :
                    # On met à jour le joueur et le num du tour
                    self.tour_joueur = - self.tour_joueur 
                    self.tour_nb += 1
                    fenetre2.after(2000,self.jeu_avec_affichage)
                else:
                    self.resultat = self.liste_othellier[-1].gagnant 
                    fenetre2.after(2000,self.afficher_gagnant)
            
            else :
                canvas2.delete("all")
                self.liste_othellier[-1].afficher()
                event_var = IntVar()

                def choisir_position(event):
                    print("event :",event)
                    x = event.x
                    y = event.y
                    for i in range(8):
                        for j in range(8):
                            if (x > 10+i*long) and (x < 10+(i+1)*long) and (y >10+j*long) and (y < 10+(j+1)*long):
                                coord_choisies = [j,i]
                    index_successeur = 0
                    for coord in self.liste_othellier[-1].liste_coord_successeurs:
                        if coord == coord_choisies:
                            print("coord choisies")
                            print("len(self.liste_othellier)",len(self.liste_othellier))
                            self.liste_othellier.append(Othellier(self.joueurs[self.tour_joueur].prof_adv,-self.tour_joueur,self.liste_othellier[-1].liste_successeurs[index_successeur].tablier,self.liste_othellier[-1].liste_successeurs[index_successeur].precedent_passe))
                            
                            # On affiche le nouvel othellier
                            canvas2.delete("all")
                            self.liste_othellier[-1].afficher()
                            
                            event_var.set(1) 
                        index_successeur += 1

                
                canvas2.bind('<Button-1>',choisir_position)
                canvas2.focus_set()

                # On relance jeu_avec_affichage dès qu'il y a eu clic ou bouton
                fenetre2.wait_variable(event_var)

                def rien(event):
                    print("rien")
                # Dès qu'on a fini le tour, on bind le clique à une fonction qui ne fait rien pour pas que ça pose de problème si on clique sans faire exprès
                canvas2.bind('<Button-1>',rien)

                # On relance gam_with_display
                if self.liste_othellier[-1].gagnant == 0 :
                    # On met à jour le joueur et le num du tour
                    self.tour_joueur = - self.tour_joueur 
                    self.tour_nb += 1
                    fenetre2.after(2000,self.jeu_avec_affichage)
                else:
                    self.resultat = self.liste_othellier[-1].gagnant 
                    fenetre2.after(2000,self.afficher_gagnant)

        # Cas où une IA joue à ce tour
        else:
            # On ajoute le nouvel othellier
            self.liste_othellier.append(self.joueurs[self.tour_joueur].jouer(self.liste_othellier[-1]))

            # On affiche le nouvel othellier
            canvas2.delete("all")
            self.liste_othellier[-1].afficher()


            if self.liste_othellier[-1].gagnant == 0 :
                # On met à jour le joueur et le num du tour
                self.tour_joueur = - self.tour_joueur 
                self.tour_nb += 1
                fenetre2.after(1000,self.jeu_avec_affichage)
            else:
                self.resultat = self.liste_othellier[-1].gagnant 
                fenetre2.after(500,self.afficher_gagnant)



########################## Classe Joueur #####################################
class Joueur(object):

    def __init__(self,couleur = 1,IA = True,IAtype = 'MinMax', prof = 1,prof_adv = 1,MCTS_N =50,MCTS_T = 3,MCTS_C = 2,advisMCTS = False):
        """
        Crée les attributs avec les valeurs prises en argument.
        """
        self.couleur = couleur # Joueur 1 ou joueur -1
        self.IA = IA # Boléen pour savoir si c'est un joueur IA (true) ou un vrai joueur (false)
        self.IAtype = IAtype # Si c'est un IA, quel type d'IA : MinMax, AlphaBeta, MCTS (MinMax par défaut)
        self.prof = prof # Si c'est un IA, la profondeur d'exploration (3 par défaut)
        self.prof_adv = prof_adv # Si l'adversaire est un IA, on donne la profondeur d'exploration de l'adversaire 
        self.MCTS_N = MCTS_N # Si c'est un IA MCTS, le nombre de simulation (50 par défaut)
        self.MCTS_T = MCTS_T # Nombre de simulations de parties aléatoires pendant le processus MCTS
        self.MCTS_C = MCTS_C # Paramètre C pour le calcul de l'UCB
        self.advisMCTS = advisMCTS # L'adversaire joue-t-il un algo MCTS ? (Change la profondeur de l'othellier retourné par l'adversaire)

    def jouer(self,othellier):
        """
        Prend en entrée un othellier et retourne l’othellier obtenu à l’issue du coup du joueur. 
        Selon l’algorithme choisi pour ce joueur, une méthode différente est appelée : jouerMinMax(), jouerAlphaBeta ou jouerMCTS().
        Entrée : Instance de la classe joueur, instance de la classe othellier
        Sortie : Instance de la classe Othellier
        """
        # Selon les types de joueurs, on appelle differentes fonctions de choix du move à faire
        if self.IAtype == 'MinMax' : 
            return self.jouerMinMax(othellier)
        if self.IAtype == 'AlphaBeta' : 
            return self.jouerAlphaBeta(othellier)
        if self.IAtype == 'MCTS' : 
            return self.jouerMCTS(othellier)
        if self.IAtype == "Hasard":
            return self.jouerHasard(othellier)


    def jouerHasard(self,othellier):
        """"
        Prend en entrée un othellier et retourne l’othellier obtenu à l’issue du coup du joueur en choisissant le coup au hasard parmis les coups possibles.
        Entrée : Instance de la classe joueur, instance de la classe othellier
        Sortie : Instance de la classe Othellier
        """
        choix = randint(0,len(othellier.liste_successeurs)-1)
        return Othellier(self.prof_adv,-self.couleur,othellier.liste_successeurs[choix].tablier,othellier.liste_successeurs[choix].precedent_passe,self.advisMCTS)


    def jouerMinMax(self,othellier):
        """
        Prend en entrée un othellier et retourne l’othellier obtenu à l’issue du coup du joueur en utilisant la fonctions MinMax() qui est codée par ailleurs.
        Entrée : Instance de la classe joueur, instance de la classe othellier
        Sortie : Instance de la classe Othellier
        """

        # Pour gérer le cas où il n'y a qu'1 seul successeur possible on le joue direct
        if len(othellier.liste_successeurs) == 1:
            return Othellier (self.prof_adv,-self.couleur,othellier.liste_successeurs[0].tablier,othellier.liste_successeurs[0].precedent_passe,self.advisMCTS)

        # On initialise le score max à une valeur très basse
        bestScore = -10000

        bestMove = []
        ppasse = []

        # On va parcourir les successeurs de l'othellier actuel
        # C'est un de ces successeurs que l'on va choisir, il faut donc les évaluer.
        for son in othellier.liste_successeurs: 
            # On les évalue avec la fonction MinMax qui va s'occuper de faire remonter la valeur de l'othellier successeur
            # On est donc un étage plus bas sur l'arbre que l'othellier initial (d'où prof-1)
            # On est sur un étage Max, le prochain sera donc un étage Min (d'où le -joueur et False)
            score = MinMax(son,self.prof-1,-self.couleur,False,self.couleur)
            if score > bestScore : 
                bestScore = score
                bestMove = [son.tablier]
                ppasse = [son.precedent_passe]
            elif score == bestScore:
                bestMove.append(son.tablier)
                ppasse.append(son.precedent_passe)
        #Parmis les meilleurs coups, choisi au hasard. 
        choix = randint(0,len(bestMove)-1)
        return Othellier(self.prof_adv,-self.couleur,bestMove[choix],ppasse[choix],self.advisMCTS)


    def jouerAlphaBeta(self,othellier):
        """
        Prend en entrée un othellier et retourne l’othellier obtenu à l’issue du coup du joueur en utilisant la fonctions AlphaBeta() qui est codée par ailleurs.
        Entrée : Instance de la classe joueur, instance de la classe othellier
        Sortie : Instance de la classe Othellier
        """

        # Pour gérer le cas où il n'y a qu'1 seul successeur possible on le joue direct
        if len(othellier.liste_successeurs) == 1:
            return Othellier (self.prof_adv,-self.couleur,othellier.liste_successeurs[0].tablier,othellier.liste_successeurs[0].precedent_passe,self.advisMCTS)

        # Pour gérer le cas où prof = 1 -> on retourne juste le max des successeurs
        if self.prof == 1:
            best_score = -1001
            bestMove = othellier.liste_successeurs[0].tablier
            bestMove = []
            ppasse = []
            for son in othellier.liste_successeurs:

                if son.gagnant == self.couleur :
                    othellier.score = 1000
                elif son.gagnant == -self.couleur : 
                    son.score = -1000
                else:
                    son.score = son.evaluate(self.couleur)
            
                if son.score > best_score:
                    best_score = son.score
                    bestMove = [son.tablier]
                    ppasse = [son.precedent_passe]
                elif son.score == best_score:
                    bestMove.append(son.tablier)
                    ppasse.append(son.precedent_passe)

            choix = randint(0,len(bestMove)-1)
            return Othellier(self.prof_adv,-self.couleur,bestMove[choix],ppasse[choix],self.advisMCTS)

        # Initialisation de alpha et beta
        alpha = -100000000
        beta = 100000000
        ppasse = False
        # On lance alpha-beta qui retourne le score de l'othellier cible vers lequel on doit aller
        score_alpha_beta = AlphaBeta(othellier,self.prof,self.couleur,alpha,beta,True,self.couleur)

        # On détermine quel othellier jouer pour être sur la branche qui mène à l'othellier cible dont le score est score_alpha_beta
        liste_othelliers_score_egal = []
        for othellier_a_jouer in othellier.liste_successeurs:
            liste_successeurs_prof_i = othellier_a_jouer.liste_successeurs
        
            for i in range(1,self.prof):  

                liste_successeurs_prof_i_plus_1 = []
                for successeur in liste_successeurs_prof_i:
                    if successeur.score == score_alpha_beta:
                        liste_othelliers_score_egal.append([othellier_a_jouer.tablier,othellier_a_jouer.precedent_passe])
                    if i < self.prof-1: 
                        for successeur_de_successeur in successeur.liste_successeurs:
                            liste_successeurs_prof_i_plus_1.append(successeur_de_successeur)
                liste_successeurs_prof_i = liste_successeurs_prof_i_plus_1.copy()

        choix = randint(0,len(liste_othelliers_score_egal)-1)
        return Othellier(self.prof_adv,-self.couleur,liste_othelliers_score_egal[choix][0],liste_othelliers_score_egal[choix][1],self.advisMCTS)

    def jouerMCTS(self, othellier):
        """
        Prend en entrée un othellier et retourne l’othellier obtenu à l’issue du coup du joueur en utilisant la fonctions MCTS() qui est codée par ailleurs.
        Entrée : Instance de la classe joueur, instance de la classe othellier
        Sortie : Instance de la classe Othellier
        """
        # On initialise le score max à une valeur très basse
        bestScore = -10000
        # On initialise le tablier de sortie comme on veut
        bestMove = np.array([[0 for i in range(8)] for j in range(8)])
        othellier_MCTS = Othellier(1, othellier.joueur, othellier.tablier, othellier.precedent_passe, isMCTS=TRUE)
        for N in range(1, self.MCTS_N+1):  # on fait N fois le processus de MCTS
            MCTS(othellier_MCTS, self.MCTS_C, N, self.MCTS_T)

        ppasse = FALSE
        # On va parcourir les successeurs de l'othellier actuel
        # C'est un de ces successeurs que l'on va choisir, il faut donc les évaluer
        # Calcul des UCB des successeurs      
        if othellier_MCTS.liste_successeurs != []:
            scores = []
            for successeur in othellier_MCTS.liste_successeurs:
                if successeur.n != 0:
                    scores.append(successeur.t/successeur.n + self.MCTS_C *
                                np.sqrt(np.log(self.MCTS_N)/successeur.n)) 
                else:  
                    scores.append(successeur.t)
            score_max = max(scores)

            liste_argmax = [i for i, j in enumerate(scores) if j == score_max]
            size_score_max = len(liste_argmax)            
            bestScore = liste_argmax[randint(0, size_score_max-1)]
            # Ici, on cherche à maximiser le score du joueur, donc si le score dépasse le score max jusqu'à là,
            # On change le best score et on retient le tablier du successeurs qui a ce nouveau score max
            bestMove = othellier_MCTS.liste_successeurs[bestScore].tablier
            ppasse = othellier_MCTS.liste_successeurs[bestScore].precedent_passe
        else: # Permet de gérer le cas en fin de partie où il n'y a plus de successeurs OU s'il n'y a aucun coup jouable pendant la partie
            bestMove = othellier_MCTS.tablier
            ppasse = othellier_MCTS.precedent_passe
            couleur = -self.couleur
        return Othellier(self.prof_adv, -self.couleur, bestMove, ppasse, isMCTS=FALSE)


########################## Fonctions Annexes #####################################


def MinMax(othellier,prof,joueur,isMaximizing,joueur_origine):
    """"
    Fonction de l'algorithme MinMax, appellée de manière récursive jusqu'à arriver soit à des othelliers terminaux (gagnant/perdant), soit atteindre la profondeur maximale d'exploration. 
    Permet de faire remonter la valeur d'une branche. 
    Entrée : Instance de la classe Othellier, profondeur restante à explorer, bolléen indiquant si c'est un noeud min ou un noeud max et le numéro du joueur dont c'est le tour. 
    Sortie : Score évaluant la branche. 
    """
    #Conditions d'arrêts et scores à remonter 
    #Si l'othellier est gagnant, on remonte un valeur très élevé 1000
    if othellier.gagnant == joueur_origine : 
        return 1000
    #Si il est perdant, on remonte une valeur très faible -1000
    if othellier.gagnant == -joueur_origine : 
        return -1000
    #Si l'othellier n'est pas terminal, et que l'on a atteint la profondeur max: 
    # on s'arrête et on utilise la fonction d'evaluation pour connaitre le score à remonter
    if (prof == 0) : 
        return (othellier.evaluate(joueur_origine))

    #Tant que l'on est dans aucun de ces cas : 
    #Si on est sur un noeud max 
    if isMaximizing : 
        bestscore = -10000
        #Pour chaque successeurs, on relance MinMax
        for son in othellier.liste_successeurs : 
            #On était sur un noeud max, les noeuds successeurs seront donc des noeuds min
            score = MinMax(son,prof-1,-joueur,False,joueur_origine) #recursion
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
            score = MinMax(son,prof-1,-joueur,True,joueur_origine) #recursion
            #On remonte le score minimal
            if score < bestscore: 
                bestscore = score
        return bestscore



def AlphaBeta(othellier,prof,joueur,alpha,beta,isMaximizing,joueur_origine):
    """
    Fonction de l'algorithme AlphaBeta, appellée de manière récursive jusqu'à arriver soit à des othelliers terminaux (gagnant/perdant), soit atteindre la profondeur maximale d'exploration. 
    Permet de faire remonter la valeur d'une branche. 
    Entrée : Instance de la classe Othellier, profondeur restante à explorer, les valeurs actuels de alpha et beta, un bolléen indiquant si c'est un noeud min ou un noeud max et le numéro du joueur dont c'est le tour. 
    Sortie : Score évaluant la branche.  
    """

    #Si l'othellier est gagnant, on remonte un valeur très élevé 1000
    if othellier.gagnant == joueur_origine :
        othellier.score = 1000
        return 1000
    #Si il est perdant, on remonte une valeur très faible -1000
    if othellier.gagnant == -joueur_origine : 
        othellier.score = -1000
        return -1000

    #Si l'othellier n'est pas terminal, et que l'on a atteint la profondeur max ou qu'il n'y a pas de successeur: 
    # on s'arrête et on utilise la fonction d'evaluation pour connaitre le score à remonter
    if (prof == 0) or (othellier.liste_successeurs == []): 
        othellier.score = othellier.evaluate(joueur_origine)
        return othellier.score

    #Si on est sur un noeud max 
    if isMaximizing:
        #Pour chaque successeurs, on relance AlphaBeta
        for son in othellier.liste_successeurs :
            score = AlphaBeta(son,prof-1,-joueur,alpha,beta,False,joueur_origine)
            if score > alpha:
                alpha = score
                if alpha >= beta:
                    break
        return alpha
    #Si on est sur un noeud min
    else: 
        #Pour chaque successeurs, on relance AlphaBeta
        for son in othellier.liste_successeurs :
            score = AlphaBeta(son,prof-1,-joueur,alpha,beta,True,joueur_origine)
            if score < beta:
                beta = score
                if alpha >= beta:
                    break
        return beta


def MCTS(othellier, C, N, T):  
    """
    Cette fonction ne return rien, elle est là pour chercher les successeurs de l'othellier en jeu, lancer des simulations et mettre les scores des successeurs à jour
    """
    othelliers_choisis = [othellier] # L'othellier d'entrée est l'othellier racine de l'algo MCTS
    joueur_principal = othellier.joueur # On retient également le joueur d'entrée car c'est par rapport à lui qu'on va calculer les scores
   
    othellier_pere = othellier
    while othelliers_choisis[-1].n > 1 and othelliers_choisis[-1].liste_successeurs != []: 
    # Tant qu'on est sur un othellier qui a été visité AU MOINS 1 fois donc qui a au moins eu une expansion ou plus

        ######## SELECTION #########
        # On parcourt les scores des othelliers successeurs
        liste_scores_successeurs = []
        for successeur in othellier_pere.liste_successeurs:  
            if successeur.n != 0:  
                liste_scores_successeurs.append(successeur.t/successeur.n + C * np.sqrt(np.log(N)/successeur.n))  
            else:  
                liste_scores_successeurs.append(successeur.t)

        # Choix du successeur le plus prometteur
        score_max = max([scores for scores in liste_scores_successeurs])

        # Si le score max apparait plus d'une fois, on choisit un successeurs au hasard parmis ceux de score max

        liste_argmax = [i for i, j in enumerate(liste_scores_successeurs) if j == score_max]
        nb_max = len(liste_argmax)
        successeur_choisi = liste_argmax[randint(0, nb_max-1)]
        othellier_choisi = othellier_pere.liste_successeurs[successeur_choisi]
        othelliers_choisis.append(othellier_choisi)

        othellier_choisi.isMCTS=TRUE # Permet de ne calculer que les successeurs à profondeur 1 (économie de mémoire)
        othellier_choisi.liste_successeurs = []
        othellier_choisi.successeurs_bis()
        othellier_pere = othellier_choisi


    othellier_joue = othelliers_choisis[-1]
    othellier_joue.isMCTS = TRUE 
    othellier_joue.liste_successeurs = [] # Il se peut que la liste soit non vide car atteinte de profmax, donc on la vide

    othellier_joue.successeurs_bis() 
    
    ######## EXPANSION #########
    if othellier_joue.liste_successeurs != []:
        othellier_expansion = othellier_joue.liste_successeurs[randint(0, len(othellier_joue.liste_successeurs)-1)]
        joueur_expansion = othellier_expansion.joueur

        ########## SIMULATION ##########
        for simu_aleatoire in range(T):
            othellier_final = simulation_MCTS(
                othellier_expansion, joueur_expansion)

        ########## RETRO PROPAGATION ##########
        # Actualisation de n pour le noeud joué
            othellier_expansion.n += 1

        # Actualisation de t pour le noeud joué
            if othellier_final.gagnant == joueur_principal:  # Si le joueur principal gagne la partie
                score = 1
                if othellier_expansion.t == 10000: 
                    othellier_expansion.t = score  
                else:
                    othellier_expansion.t += score
            elif othellier_final.gagnant == 2:
                score = 0
                if othellier_expansion.t == 10000: 
                    othellier_expansion.t = score 
                else:
                    othellier_expansion.t += score
            elif othellier_final.gagnant == -joueur_principal:
                score = -1
                if othellier_expansion.t == 10000:
                    othellier_expansion.t = score
                else:
                    othellier_expansion.t += score

            for othellier_i in othelliers_choisis:
                othellier_i.n += 1
                if othellier_i.t == 10000:
                    othellier_i.t = score
                else:
                    othellier_i.t += score 
    else:  # Si on est à la fin de l'arbre
        pass


def simulation_MCTS(othellier, joueur):
    """
    Cette fonction sert à faire les simulations aléatoires de MCTS à partir de l'othellier d'expansion prit en entrée
    """
    tablier_0 = othellier.tablier # Tablier de l'othellier d'expansion
    othellier_0 = Othellier(1, joueur, tablier_0) # Création d'un othellier à partir de ce tablier pour avoir ses successeurs
    othellier_joue = othellier_0
    joueur = othellier_0.joueur  
    # Boucle de jeu
    # Si les deux joueurs passent successivement, c'est qu'on ne peut plus jouer, on arrête
    while othellier_joue.gagnant == 0:
        nbr_successeurs = len(othellier_joue.liste_successeurs)
        successeur_aleatoire = othellier_joue.liste_successeurs[randint(0, nbr_successeurs-1)]
        othellier_joue = (Othellier(1, -joueur, successeur_aleatoire.tablier, successeur_aleatoire.precedent_passe)) # L'othellier en jeu change
        joueur = -joueur 
    return(othellier_joue)


def lancer_une_partie():
    """
    Ferme toute fenêtre existante et lance une partie en créant une instance de la classe partie. 
    """
    fenetre.destroy()
    partie_1 = Partie()


def simulation_n_parties():
    """
    Permet de lancer un grand nombre de parties d'un coup et récupèrer les résultats de ces parties. 
    
    """
    fenetre.destroy()
    fenetre2 = tk.Tk() # crée une fenêter sur laquelle on va pouvoir travailler
    fenetre2.configure(height = 20*long, width = 20*long) # Règle les paramètres de la fenêtre --> laisse une marge de 3*long autour du tablier
    canvas2 = tk.Canvas(fenetre2, width=10*long, height=10*long, background='white')

    nb_simulation = 1
    nb_victoires = ["Victoires : ",0,0,0] # Position 1 = joueur 1, position 2 = égalité, et position -1 = joueur -1.
    
    while nb_simulation < 51:
        # print("nb_simulation",nb_simulation)

        partie_i = Partie(False)
        nb_victoires[partie_i.resultat] += 1 # on ajoute 1 victoire au gagnant

        if partie_i.resultat == 2:
            canvas2.create_text(10+4*long,10+nb_simulation*long/3, text = "Partie {} : il y a égalité. Total J1 : {}, total J2 : {}, total égalités : {}".format(nb_simulation,nb_victoires[1],nb_victoires[-1],nb_victoires[2]))
        else:
            canvas2.create_text(10+4*long,10+nb_simulation*long/3, text = "Partie {} : le joueur {} a gagné. Total J1 : {}, total J2 : {}, total égalités : {}".format(nb_simulation,partie_i.result,nb_victoires[1],nb_victoires[-1],nb_victoires[2]))

        nb_simulation += 1
    
    canvas2.pack()
    fenetre2.mainloop()


###########################
### PROGRAMME PRINCIPAL  qu'on va rendre ###
###########################

global long
long = 80

fenetre = tk.Tk() # crée une fenêter sur laquelle on va pouvoir travailler
fenetre.configure(height = 20*long, width = 20*long) # Règle les paramètres de la fenêtre --> laisse une marge de 3*long autour du tablier

canvas = tk.Canvas(fenetre, width=10*long, height=10*long, background='white')

label = tk.Label(fenetre, text="Qui voulez-vous voir jouer ? Avec quels paramètres ?", font=("Helvetica", 20))
label.place(x = 10 + 4*long, y = 10 + long)

type_joueur = ["humain","machine"]
type_1 = StringVar()
label = tk.Label(fenetre, text="Joueur blanc", font=("Helvetica", 20))
label.place(x = 10 + 5*long, y = 10 + 2*long)
widget = ttk.Combobox(fenetre, textvariable = type_1, values=type_joueur)
widget.current(1)
widget['state'] = 'readonly'
widget.place(x = 10 + 4*long, y= 3*long)
type_2 = StringVar()
label = tk.Label(fenetre, text="Joueur noir", font=("Helvetica", 20))
label.place(x = 10 + 8*long, y = 10 + 2*long)
widget = ttk.Combobox(fenetre, textvariable = type_2, values=type_joueur)
widget.current(1)
widget['state'] = 'readonly'
widget.place(x = 10 + 7*long, y= 3*long)


IAtype = ["MinMax","AlphaBeta","MCTS","Hasard"]
IAtype_1 = StringVar()
label = tk.Label(fenetre, text="Quel algorithme ?", font=("Helvetica", 16))
label.place(x = 10 + 2*long, y = 4*long)
widget = ttk.Combobox(fenetre, textvariable = IAtype_1, values=IAtype)
# widget.current(0) # ne rien mettre par défaut sinon quand on met joueur humain il faut aussi changer ça
widget['state'] = 'readonly'
widget.place(x = 10 + 4*long, y= 4*long)
IAtype_2 = StringVar()
widget = ttk.Combobox(fenetre, textvariable = IAtype_2, values=IAtype)
# widget.current(0)
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


label = tk.Label(fenetre, text="MCTS : nombre d'itérations Sélection-Expansion-Simulation-Rétropropagation ?", font=("Helvetica", 16))
label.place(x = 10 + long, y = 6*long)
MCTS_N_1 = tk.IntVar()
MCTS_N_1.set(10)
widget = tk.Scale(fenetre, variable=MCTS_N_1, orient='horizontal', from_=1, to=100, resolution=1, tickinterval=25, length=100)
widget.place(x = 10 + 5*long, y = 6*long)
MCTS_N_2 = tk.IntVar()
MCTS_N_2.set(10)
widget = tk.Scale(fenetre, variable=MCTS_N_2, orient='horizontal', from_=1, to=100, resolution=1, tickinterval=25, length=100)
widget.place(x = 10 + 8*long, y = 6*long)


label = tk.Label(fenetre, text="MCTS : nombre de simulations de parties aléatoires ?", font=("Helvetica", 16))
label.place(x = 10 + long, y = 7*long)
MCTS_T_1 = tk.IntVar()
MCTS_T_1.set(5)
widget = tk.Scale(fenetre, variable=MCTS_T_1, orient='horizontal', from_=1, to=100, resolution=1, tickinterval=1, length=100)
widget.place(x = 10 + 5*long, y = 7*long)
MCTS_T_2 = tk.IntVar()
MCTS_T_2.set(5)
widget = tk.Scale(fenetre, variable=MCTS_T_2, orient='horizontal', from_=1, to=100, resolution=1, tickinterval=1, length=100)
widget.place(x = 10 + 8*long, y = 7*long)


label = tk.Label(fenetre, text="MCTS : paramètre C ?", font=("Helvetica", 16))
label.place(x = 10 + long, y = 8*long)
MCTS_C_1 = tk.IntVar()
MCTS_C_1.set(2)
widget = tk.Scale(fenetre, variable=MCTS_C_1, orient='horizontal', from_=1, to=10, resolution=1, tickinterval=0.25, length=100)
widget.place(x = 10 + 5*long, y = 8*long)
MCTS_C_2 = tk.IntVar()
MCTS_C_2.set(2)
widget = tk.Scale(fenetre, variable=MCTS_C_2, orient='horizontal', from_=1, to=10, resolution=1, tickinterval=0.25, length=100)
widget.place(x = 10 + 8*long, y = 8*long)

bouton = tk.Button(fenetre, text="Jouer / visualiser le déroulement d'une partie", command = lancer_une_partie)
bouton.place(x = 2*long, y= 9*long)

bouton = tk.Button(fenetre, text="Lancer 50 simulations avec ces paramètres (que pour machine VS machine)", command = simulation_n_parties)
bouton.place(x = 8*long, y= 9*long)

canvas.pack()
fenetre.mainloop()




