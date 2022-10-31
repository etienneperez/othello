
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


########################## MCTS ###########################

def MCTS(othellier, prof, C, T, i): # j'ai mis T ici dans l'idée qu'on va mettre la fonction MCTS en boucle avec un T qui augmente en dehors de l'appel de fonction
    ### Si on est au tout début du jeu, on va choisir l'othellier suivant au hasard car aucun othellier n'a été visité donc tous les UCB valent + l'infini
    #if othellier == othellier_0:
    if i == 0:
        # choix d'un othellier successeur au hasard puisque toutes les valeurs d'UCB valent + l'infini
        othelliers_choisis = [othellier]
        # ici au lieu de juste aller a prof max on voudrait aussi avoir une condition sur passe, un truc du genre
        # while prof_i < othellier.prof+1 OR passe < 2: (avec incrémentation de prof_i) mais pas encore sure de comment faire fonctionner ça
        prof_i = 1
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
        if othellier_final.gagnant == joueur: # si ce joueur gagne la partie
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
            
            if liste_scores_successeurs == []:
                return("Fin de partie")
            else:
                successeur_choisi = np.argmax(liste_scores_successeurs) # retourne l'indice de l'UCB le plus élevé, les successeurs 
                                                                 # étant parcourus dans l'ordre on sait à quel successeur ça correspond
                othellier_choisi = othellier_pere.liste_successeurs[successeur_choisi]
                othellier_choisi.n += 1 # l'othellier choisi est visité une fois
                othelliers_choisis.append(othellier_choisi) # ajouté à la liste des othelliers visités
            
                othellier = othellier_choisi 
                prof_i += 1
        
            joueur = othellier.joueur # maintenant qu'on sait de quel othellier on part on sait qui joue et on peut lancer la partie aléatoire
            othellier_final = game_MCTS(othellier, 1, joueur)    
            if othellier_final.gagnant == joueur: # si ce joueur gagne la partie
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
    # Boucle de jeu
    while liste_othellier_partie[i].gagnant == 0 : #si les deux joueurs passent successivement, c'est qu'on ne peut plus jouer, on arrête
        print("tablier MCTS", liste_othellier_partie[i].tablier)
        #liste_othellier_partie.append(compMove(liste_othellier_partie[i],prof,joueur))
        nbr_successeurs = len(liste_othellier_partie[i].liste_successeurs)
        successeur_aleatoire = liste_othellier_partie[i].liste_successeurs[randint(0, nbr_successeurs-1)]
        liste_othellier_partie.append(Othellier(1, -joueur, successeur_aleatoire.tablier, successeur_aleatoire.precedent_passe)) 
        joueur = -joueur #changement de joueur
        i += 1
    return(liste_othellier_partie[-1])