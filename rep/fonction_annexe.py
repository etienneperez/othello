
##########Fonction MinMax#################
#Cette fonction va faire remonter le valeur d'une branche
#Elle fonctionne par recursion jusqu'à atteindre soit la profondeur max d'exploration, soit un othellier terminal
#La recursion alterne entre des étages min et des étages max
def MinMax(othellier,prof,joueur,isMaximizing):
    #Conditions d'arrêts et scores à remonter 
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

def MCTS(othellier, prof, C, N): # j'ai mis N ici dans l'idée qu'on va mettre la fonction MCTS en boucle avec un N qui augmente en dehors de l'appel de fonction
    othelliers_choisis = [othellier]
    while othelliers_choisis[-1].n > 1: # tant qu'on est sur un othellier qui a été visité AU MOINS 2 fois donc qui a au moins eu une expansion
        othellier_pere = othellier 
        othellier_pere.n += 1
            
        # là on va regarder les valeurs d'UCB des successeurs, mais s'ils n'ont pas été visité leur t vaudra 10000 donc on vérifie
        # si plusieurs n'ont pas été visités ils auront forcément tous des valeurs d'UCB infinie donc on prendra au hasard parmi ceux encore non visités
        # s'ils ont tous été visités on prend la valeur max des UCB 
        
        ######## SELECTION et EXPANSION #########

        ## cette liste permet pour chaque othellier visité de sélectionner son successeur le plus prometteur
        # construction de la liste
        liste_scores_successeurs = []
        for successeur in othellier_pere.liste_successeurs: # parmi les successeurs de l'othellier père
            if successeur.n != 0: # si le noeud successeur a été vu au moins une fois 
                liste_scores_successeurs.append(successeur.t/successeur.n + C * np.sqrt(np.log(N)/successeur.n)) # calcul de l'UCB
            else: # le noeud n'a jamais été visité, son score vaut t = 100000
                liste_scores_successeurs.append(successeur.t)
            
        if liste_scores_successeurs == []: # en fin de partie pour éviter une erreur
            return("Fin de partie")
        
        # choix du successeur le plus prometteur
        else:
            score_max = max([scores for scores in liste_scores_successeurs]) # sélection du score le plus élevé

            # ce score peut apparaître plusieurs fois, si oui on veut choisir au hasard parmi ces différentes occurences 
            # ce qui revient à choisir un successeur au hasard parmi les plus prometteurs

            liste_argmax = [i for i, j in enumerate(liste_scores_successeurs) if j == score_max] 
                    # liste des indices d'où se trouve le maximum dans liste_scores_successeurs
            nb_max = len(liste_argmax) 
                    # on va choisir au hasard un indice dans cette liste pour récupérer un des maximum (s'il y en a plusieurs)
            successeur_choisi = liste_argmax[randint(0,nb_max-1)]   # retourne un indice d'UCB le plus élevé, les successeurs 
                                                                    # étant parcourus dans l'ordre on sait à quel successeur ça correspond
            othellier_choisi = othellier_pere.liste_successeurs[successeur_choisi]
            othelliers_choisis.append(othellier_choisi) # ajouté à la liste des othelliers visités

            # l'othellier successeur choisi est construit comme un nouvel othellier dont on recalcule les successeurs sur 1 profondeur pour l'adversaire
            othellier = Othellier(1, -othellier_choisi.joueur, othellier_choisi.tablier, othellier_choisi.precedent_passe)

     # en sortie de boucle on est donc soit sur un othellier qui n'a jamais été visité (n=0) et donc fait une simulation
     # soit un othellier visité une fois qui a été le résultat d'une expansion

    othellier_joue = othelliers_choisis[-1]
    joueur = othellier_joue.joueur # maintenant qu'on sait de quel othellier on part on sait qui joue et on peut lancer la partie aléatoire

    ########## SIMULATION ##########

    othellier_final = simulation_MCTS(othellier_joue, 1, joueur)    

    ########## RETRO PROPAGATION jusqu'à l'othellier duquel est parti le MCTS ##########

    # ici on considère que si la partie est gagnée pour le joueur 1, l'othellier duquel est parti la simulation voit son score t actualisé
    # une partie gagnée = un score t incrémenté de 1
    # à l'inverse, une partie perdue = un score t qui diminue de 1

    # actualisation de n pour le noeud joué
    othellier_joue.n += 1

    # actualisation de t pour le noeud joué
    if othellier_final.gagnant == joueur: # si ce joueur gagne la partie
        score = 1
        if othellier_joue.t == 10000: # si le noeud est visité pour la première fois, son score initial est de 10000
            othellier_joue.t = score # l'othellier duquel le jeu est parti prend 1
        else:
            othellier_joue.t += score 
    elif othellier_final.gagnant == 2: # en cas d'égalité
        score = 0
    elif othellier_final.gagnant == -joueur:
        score = -1
        if othellier_joue.t == 10000:
             othellier_joue.t = score
        else:
            othellier_joue.t += score # en cas de défaite

    # maintenant on veut faire remonter l'information sur la victoire/défaite après la partie aléatoire grâce à la liste othelliers_choisis

    del(othelliers_choisis[-1]) # on a déjà actualisé les valeurs de l'othellier sur lequel on a joué

    for othellier in othelliers_choisis:
        othellier.n += 1
        if othellier.t == 10000:
            othellier.t = score
        else:
            othellier.t += score # tous les othelliers qui ont été choisis pour arriver à l'othellier duquel la partie aléatoire a été lancée ont leur score modifié


## jeu aléatoire partant d'un othellier prédterminé

def simulation_MCTS(othellier, prof, joueur):
    tablier_0 = othellier.tablier
    othellier_0 = Othellier(prof, joueur, tablier_0)
    liste_othellier_partie = [othellier_0]

    #initialisations
    i = 0 #compteur de tour
    joueur = othellier_0.joueur #A qui le tour ? 
    # Boucle de jeu
    while liste_othellier_partie[i].gagnant == 0 : #si les deux joueurs passent successivement, c'est qu'on ne peut plus jouer, on arrête
        #liste_othellier_partie.append(compMove(liste_othellier_partie[i],prof,joueur))
        nbr_successeurs = len(liste_othellier_partie[i].liste_successeurs)
        successeur_aleatoire = liste_othellier_partie[i].liste_successeurs[randint(0, nbr_successeurs-1)]
        liste_othellier_partie.append(Othellier(1, -joueur, successeur_aleatoire.tablier, successeur_aleatoire.precedent_passe)) 
        joueur = -joueur #changement de joueur
        i += 1
    return(liste_othellier_partie[-1])
