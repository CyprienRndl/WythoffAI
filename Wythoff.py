
import random
import copy
import time


"""
    Training et mise en place d'une IA sur le jeu de Wythoff

"""


##############################
##      Préparation IA      ##
##############################


def affiche_plateau(plateau):
    """ Affiche le plateau

    Args:
        plateau (tab[][]): plateau sur lequel le jeu se déroule
    """
    LINE_LENGTH = len(plateau) # taille ligne
    COLUMN_LENGTH = len(plateau[0]) # taille colonne

    # Affiche l'index Y et le plateau
    for i in range((LINE_LENGTH) - 1, -1, -1):
        print(i, "|", end="")
        for j in range(COLUMN_LENGTH):
            print(" " + plateau[i][j] + " |", end="")
        print()

    # Affiche l'index X
    print(" ", end="")
    for i in range(COLUMN_LENGTH):
        print(f"   {i}", end="")
    print()


def change_joueur(main_joueur, joueur1, joueur2):
    """ Change le joueur courant

    Args:
        main_joueur (String): joueur courant
        joueur1 (String): premier joueur
        joueur2 (String): deuxième joueur

    Returns:
        String: return celui qui n'étais pas le joueur courant
    """
    if main_joueur == joueur1:
        main_joueur = joueur2
    else:
        main_joueur = joueur1
    return main_joueur


def creer_plateau(lg):
    """ Créé le tableau sur lquel le jeu se déroulera

    Args:
        lg (int): longueur de la largeur du plateau

    Returns:
        tab[][]: le tableau à double entrée représentant le plateau
    """
    # Création du tableau à double entrée
    plateau = [[' ' for _ in range(lg)] for _ in range(lg)]
    return plateau


def placer_pion(plateau):
    """ Place le pion sur le plateau

    Args:
        plateau (tab[][]): plateau où placer le pion
    """
    LG = len(plateau) - 1 # longueur index du plateau
    pos_y, pos_x = 0, 0 #définition des position

    # Détermine les positions aléatoires du pion sauf si y ou x = 0 ou x = y
    while pos_y == 0 or pos_x == 0 or pos_x == pos_y:
        pos_y = random.randint(0, LG)
        pos_x = random.randint(0, LG)

    plateau[pos_y][pos_x] = 'o' # place le pion


def cherche_pos_y(plateau):
    """ Cherche la position en y du pion

    Args:
        plateau (tab[][]): plateau où chercher le pion

    Returns:
        int: la position en Y du pion
    """
    pos_y = 0

    # Parcours tout le plateau jusqu'à trouver le pion
    for i in range(len(plateau)):
        for j in range(len(plateau)):
            if plateau[i][j] == 'o':
                pos_y = i
                break  # Sortir des boucles
    return pos_y


def cherche_pos_x(plateau):
    """ Cherche la position en x du pion

    Args:
        plateau (tab[][]): plateau où chercher le pion

    Returns:
        int: la position en X du pion
    """
    pos_x = 0

    # Parcours tout le plateau jusqu'à trouver le pion
    for i in range(len(plateau)):
        for j in range(len(plateau)):
            if plateau[i][j] == 'o':
                pos_x = j
                break  # Sortir des boucles
    return pos_x


def position_gagnante(plateau):
    """ Trouve toutes les positions gagnante du plateau

    Args:
        plateau (tab[][]): plateau où se déroule le jeu

    Returns:
        tab[][]: tableau contenant les coordonnées de toutes les positions gangnante
    """
    alterne = 0  # permet d'alterner entre plusieurs actions
    count_index = 0  # compte l'index
    temp = 0
    all_positions = [[0, 0] for _ in range(int(len(plateau) * 0.8 + 0.5))]  # créé un tableau de taille optimal

    # Ajoute les positions gagnantes de la partie supérieure du plateau (a,b) au tableau all_positions
    for i in range(1, len(all_positions)):
        # Alterne successivement entre le if et le else if pour ajouter les bonnes valeurs
        if alterne == 0:
            all_positions[i][0] = all_positions[i - 1][0] + 1
            all_positions[i][1] = all_positions[i - 1][1] + 2
            if all_positions[i][0] > len(plateau) - 1 or all_positions[i][1] > len(plateau) - 1:
                all_positions[i][0] = 0
                all_positions[i][1] = 0
            alterne = 1
        elif alterne == 1:
            all_positions[i][0] = all_positions[i - 1][0] + 2
            all_positions[i][1] = all_positions[i - 1][1] + 3
            if all_positions[i][0] > len(plateau) - 1 or all_positions[i][1] > len(plateau) - 1:
                all_positions[i][0] = 0
                all_positions[i][1] = 0
            alterne = 0
        count_index += 1

    # Ajoute les inverses (b,a) au tableau all_positions
    for j in range(count_index, len(all_positions)):
        temp += 1
        all_positions[j][0] = all_positions[temp][1]
        all_positions[j][1] = all_positions[temp][0]

    return all_positions  # Retourne le tableau all_positions




def determiner_diagonale(pos_y, pos_x):
    """ Détermine les positions accessible en diagonale du pion à partir du plateau

    Args:
        pos_y (int): position du pion en Y
        pos_x (int): position du pion en X

    Returns:
        tab[][]: tableau des positions accessibles en diagonale du pion
    """
    # Création du tableau à retourner de la taille du minimum entre les deux positions
    taille = min(pos_y, pos_x)
    all_positions = [[0] * 2 for _ in range(taille)]

    # Détermine toutes les positions en diagonale du pion
    for i in range(taille):
        pos_y -= 1
        pos_x -= 1
        all_positions[i][0] = pos_y
        all_positions[i][1] = pos_x

    return all_positions  # Retourne le tableau all_positions


def determiner_gauche(pos_y, pos_x):
    """ Détermine les positions accessible à gauche du pion à partir du plateau

    Args:
        pos_y (int): position du pion en Y
        pos_x (int): position du pion en X

    Returns:
        tab[][]: tableau des positions accessibles à gauche du pion
    """
    # Création du tableau à retourner de la taille du minimum entre les deux positions
    taille = pos_x
    all_positions = [[0] * 2 for _ in range(taille)]

    # Détermine toutes les positions en diagonale du pion
    for i in range(taille):
        pos_x -= 1
        all_positions[i][0] = pos_y
        all_positions[i][1] = pos_x

    return all_positions  # Retourne le tableau all_positions


def determiner_bas(pos_y, pos_x):
    """ Détermine les positions accessible en bas du pion à partir du plateau

    Args:
        pos_y (int): position du pion en Y
        pos_x (int): position du pion en X

    Returns:
        tab[][]: tableau des positions accessibles en bas du pion
    """
    # Création du tableau à retourner de la taille du minimum entre les deux positions
    taille = pos_y
    all_positions = [[0] * 2 for _ in range(taille)]

    # Détermine toutes les positions en diagonale du pion
    for i in range(taille):
        pos_y -= 1
        all_positions[i][0] = pos_y
        all_positions[i][1] = pos_x

    return all_positions  # Retourne le tableau all_positions


def joueur_deplace_pion(plateau):
    """ Déplace le pion là où le joueur veux dans les cases accessible
        Mode de train numéro 1

    Args:
        plateau (tab[][]): plateau où le jeu se déroule
    """
    # Récupère les positions du pion
    pos_y = cherche_pos_y(plateau)
    pos_x = cherche_pos_x(plateau)

    plateau[pos_y][pos_x] = ' '  # Efface le pion du plateau

    direction = ' '
    direction_valide = False

    # Demande à l'utilisateur une direction et vérifie sa validité
    while not direction_valide:
        direction = input("Entrez une Direction (Bas = b, Gauche = g, Diagonale = d) : ").lower()

        if (pos_y == 0 and (direction == 'b' or direction == 'd')) or \
           (pos_x == 0 and (direction == 'g' or direction == 'd')):
            print("\nErreur : Vous ne pouvez pas aller dans cette direction")
        elif direction not in ['b', 'd', 'g']:
            print("\nErreur : entrez une direction valide")
        else:
            direction_valide = True

    nb_case = 0
    nb_case_valide = False

    # Demande à l'utilisateur un nombre de case et vérifie la validité
    while not nb_case_valide:
        nb_case = int(input("Entrez le nombre de cases à parcourir : "))

        if (direction == 'b' and (nb_case <= 0 or nb_case > pos_y)) or \
           (direction == 'g' and (nb_case <= 0 or nb_case > pos_x)) or \
           (direction == 'd' and (nb_case <= 0 or nb_case > pos_x or nb_case > pos_y)):
            print("\nErreur : entrez un nombre de cases à parcourir valide")
        else:
            nb_case_valide = True

    # Place le pion à la bonne position
    if direction == 'b':
        plateau[pos_y - nb_case][pos_x] = 'o'
    elif direction == 'g':
        plateau[pos_y][pos_x - nb_case] = 'o'
    elif direction == 'd':
        plateau[pos_y - nb_case][pos_x - nb_case] = 'o'


def robot_deplace_pion_alea(plateau):
    """ Déplace le pion de façon aléatoire dans les positions accessible
        Mode de train numéro 2

    Args:
        plateau (tab[][]): plateau où le jeu se déroule
    """
    # Récupère les positions du pion
    pos_y = cherche_pos_y(plateau)
    pos_x = cherche_pos_x(plateau)

    plateau[pos_y][pos_x] = ' '  # Efface le pion du plateau

    # Choix aléatoire d'une direction
    directions = ['b', 'g', 'd']
    direction = random.choice(directions)

    # Vérifie la validité de la direction
    direction_valide = False

    while not direction_valide:
        if (pos_y == 0 and (direction == 'b' or direction == 'd')) or (pos_x == 0 and (direction == 'g' or direction == 'd')):
            direction = random.choice(directions)
        elif direction not in ['b', 'd', 'g']:
            direction = random.choice(directions)
        else:
            direction_valide = True

    # Choix aléatoire d'un nombre de case
    nb_case = random.randint(0, max(pos_x, pos_y))

    # Vérifie la validité du nombre de case
    nb_case_valide = False

    while not nb_case_valide:
        if (direction == 'b' and (nb_case <= 0 or nb_case > pos_y)) or \
                (direction == 'g' and (nb_case <= 0 or nb_case > pos_x)) or \
                (direction == 'd' and (nb_case <= 0 or nb_case > pos_x or nb_case > pos_y)):
            nb_case = random.randint(0, max(pos_x, pos_y))
        else:
            nb_case_valide = True

    # Place le pion à la bonne position
    if direction == 'b':
        plateau[pos_y - nb_case][pos_x] = 'o'
    elif direction == 'g':
        plateau[pos_y][pos_x - nb_case] = 'o'
    elif direction == 'd':
        plateau[pos_y - nb_case][pos_x - nb_case] = 'o'


def robot_deplace_pion_expert(plateau):
    """ Déplace le pion de la meilleur façon possible
        Mode de train numéro 3

    Args:
        plateau (tab[][]): plateau où le jeu se déroule
    """
    pos_gagnante = position_gagnante(plateau)

    # Trouve les positions x et y du pion
    pos_y = cherche_pos_y(plateau)
    pos_x = cherche_pos_x(plateau)

    fin = False  # pour break

    # Si le pion se trouve sur un côté ou la diagonale passant par 0, déplacement en 0,0
    if pos_x == 0 or pos_y == 0 or pos_x == pos_y:
        plateau[pos_y][pos_x] = ' '  # Efface le pion du plateau
        plateau[0][0] = 'o'

    # Si le pion est à un autre positionnement, le robot déplace le pion sur la position gagnante la plus proche
    else:
        for i in range(len(pos_gagnante)):
            if pos_gagnante[i][1] == pos_y and pos_gagnante[i][0] < pos_x:
                plateau[pos_y][pos_x] = ' '  # Efface le pion du plateau
                plateau[pos_gagnante[i][1]][pos_gagnante[i][0]] = 'o'  # place le pion
                fin = True  # break

            elif pos_gagnante[i][0] == pos_x and pos_gagnante[i][1] < pos_y:
                plateau[pos_y][pos_x] = ' '  # Efface le pion du plateau
                plateau[pos_gagnante[i][1]][pos_gagnante[i][0]] = 'o'  # place le pion
                fin = True  # break

            # Pion sur une position gagnante
            elif pos_y == pos_gagnante[i][1] and pos_x == pos_gagnante[i][0]:
                robot_deplace_pion_alea(plateau)
                fin = True  # break

            else:
                diagonales = determiner_diagonale(pos_y,pos_x)  # tab des diagonales

                # Si une position en diagonale correspond à une position gagnante, déplacement
                for j in range(len(diagonales)):
                    if pos_gagnante[i][1] == diagonales[j][0] and pos_gagnante[i][0] == diagonales[j][1]:
                        plateau[pos_y][pos_x] = ' '  # Efface le pion du plateau
                        plateau[pos_gagnante[i][1]][pos_gagnante[i][0]] = 'o'  # place le pion
                        fin = True  # break

            if fin:
                break



def concatener(pos_y,pos_x):
    """ Concatene deux nombres

    Args:
        pos_y (int): nombre 1 à concatener
        pos_x (int): nombre 2 à concatener

    Returns:
        int: nombre concatener
    """
    tmp = str(pos_y) + str(pos_x)
    return int(tmp)


def jeu_joueur_contre_ia(best_pos, best_pos_score, best_dir_score):
    # Création du joueur
    ia = "ia"
    joueur1 = "joueur"

    # Détermination de qui joue en premier
    choix = input("Voulez-vous commencer à jouer ? (o/n) \n")
    while choix != 'n' and choix != 'o':
        choix = input("Voulez-vous commencer à jouer ? (o/n)\n")

    if choix == 'o':
        main_joueur = ia
    else:
        main_joueur = joueur1
    print("\nLe premier joueur à jouer est", change_joueur(main_joueur, joueur1, ia), "\n")

    # Création du plateau
    taille = 10
    plateau = creer_plateau(taille)
    affiche_plateau(plateau)

    # Placement du pion
    print("\nPlacement aléatoire du pion")
    placer_pion(plateau)

    # Joue successivement tant qu'il n'y a pas de gagnant
    while cherche_pos_x(plateau) != 0 or cherche_pos_y(plateau) != 0:
        main_joueur = change_joueur(main_joueur, joueur1, ia)
        affiche_plateau(plateau)

        print("\n", main_joueur, "Joue\n")
        if main_joueur == joueur1:
            deplace_pion(plateau)
        elif main_joueur == ia:
            ia_deplace_pion(plateau,best_pos, best_pos_score, best_dir_score)

    affiche_plateau(plateau)
    print("\n", main_joueur, "a Gagné la partie !")


def deplace_pion(plateau):
    """ Déplace le pion là où le joueur veut

    Args:
        plateau (tab[][]): plateau où le jeu se déroule
    """
    # Récupère les positions du pion
    posY = cherche_pos_y(plateau)
    posX = cherche_pos_x(plateau)

    plateau[posY][posX] = ' '  # Efface le pion du plateau

    direction = ' '
    direction_valide = False

    # Demande à l'utilisateur une direction et vérifie sa validité
    while not direction_valide:
        direction = input("Entrez une Direction (Bas = b, Gauche = g, Diagonale = d) : ").lower()

        if (posY == 0 and (direction == 'b' or direction == 'd')) or \
           (posX == 0 and (direction == 'g' or direction == 'd')):
            print("\nErreur : Vous ne pouvez pas aller dans cette direction")
        elif direction not in ['b', 'd', 'g']:
            print("\nErreur : entrez une direction valide")
        else:
            direction_valide = True

    nb_case = 0
    nb_case_valide = False

    # Demande à l'utilisateur un nombre de case et vérifie la validité
    while not nb_case_valide:
        nb_case = int(input("Entrez le nombre de cases à parcourir : "))

        if (direction == 'b' and (nb_case <= 0 or nb_case > posY)) or \
           (direction == 'g' and (nb_case <= 0 or nb_case > posX)) or \
           (direction == 'd' and (nb_case <= 0 or nb_case > posX or nb_case > posY)):
            print("\nErreur : entrez un nombre de cases à parcourir valide")
        else:
            nb_case_valide = True

    # Place le pion à la bonne position
    if direction == 'b':
        plateau[posY - nb_case][posX] = 'o'
    elif direction == 'g':
        plateau[posY][posX - nb_case] = 'o'
    elif direction == 'd':
        plateau[posY - nb_case][posX - nb_case] = 'o'



##################################
##              IA              ##
##################################
                        
### Création des scores


def creer_positions_initiales(len_plateau):
    """ Créé un tableau regroupant toutes les positions d'une plateau de longueur len_plateau

    Args:
        len_plateau (int): longueur du plateau

    Returns:
        tab[][]: tableau des positions du plateau
    """
    positions_initiale = [[pos_y, pos_x] for pos_y in range(len_plateau) for pos_x in range(len_plateau)]
    return positions_initiale


def creer_best_position(positions_initiales):
    """ Créé un tableau qui pour chaque coordonnées du plateau, défini toutes les positions accessible a partir de ce plateau ["g","b","d"]

    Args:
        positions_initiales (tab[][]): tableau de toute les positions du plateau

    Returns:
        tab[][][]: toutes les positions accessibles pour chaque coordonnées 
    """
    best_position = []

    for pos_index, position in enumerate(positions_initiales):
        pos_y, pos_x = position

        position_gauche = determiner_gauche(pos_y, pos_x)
        position_bas = determiner_bas(pos_y, pos_x)
        position_diagonale = determiner_diagonale(pos_y, pos_x)

        best_position.append([position_gauche, position_bas, position_diagonale])

    return best_position



def creer_best_position_score(best_position):
    """ Créé un tableau qui pour chaque position accessible de best_position, défini un score (par défaut : 0)

    Args:
        best_position (tab[][][]): tableau des positions accessible pour chaque coordonnée

    Returns:
        tab[][][]: tableau des scores pour chaque positions accessibles
    """
    best_position_score = copy.deepcopy(best_position)
    for i in range (len(best_position_score)):
        for j in range(len(best_position_score[i])):
            for k in range(len(best_position_score[i][j])):
                best_position_score[i][j][k] = 0
    return best_position_score



def creer_best_direction(positions_initiales):
    """ Créé un tableau qui pour chaque coordonnées du plateau, défini toutes les directions

    Args:
        positions_initiales (tab[][]): tableau de toute les positions du plateau

    Returns:
        tab[][]: tableau de des directions pour chaque coordonnées
    """
    best_direction = []
    directions = ["g","b","d"]

    for i, j in enumerate(positions_initiales):
        best_direction.append(directions)

    return best_direction


def creer_best_direction_score(best_direction):
    """ Créé un tableau qui pour chaque direction de best_direction, défini un score (par défaut : 0)

    Args:
        best_direction (tab[][]): tableau des directions pour chaque coordonnées

    Returns:
        tab[][][]: tableau des scores pour chaque directions
    """
    best_direction_score = [[0] * 3 for _ in range(len(best_direction))]
    return best_direction_score


def affiche_best_pos(best_position):
    """ Affichage simplifié des positions

    Args:
        best_position (tab[][]): tableau des positions accessible pour chaque coordonnées
    """
    for j in range (len(best_position)) :
        a = 0
        for i in range(len(best_position[j])):
            print(best_position[j][i])
            a += 1
            if(a == 3):
                print()


### Training


def ia_deplace_pion(plateau, best_pos, best_pos_score, best_dir_score):
    """ Déplacement du pion par l'IA

    Args:
        plateau (int[][]): plateau où se déroule le jeu
        best_pos (int[][]): tableau des positions accessible pour chaque coordonnées
        best_pos_score (int[][][]): tableau des scores pour chaque positions accessibles
        best_dir_score (int[][][]): tableau des scores pour chaque directions
    
    Returns:
        tab[][][]: tableau des scores pour chaque directions
    """

    # Index des directions et positions avec le plus de score
    index_max_direction = 0
    index_max_position = 0

    # positions du pion
    pos_y = cherche_pos_y(plateau)
    pos_x = cherche_pos_x(plateau)

    plateau[pos_y][pos_x] = ' '  # Efface le pion du plateau

    # index de la position du pion
    index_pos = concatener(pos_y,pos_x)

    # défini l'index de la direction avec le plus de score
    if pos_y == 0:
        index_max_direction = 0
    elif pos_x == 0:
        index_max_direction = 1
    else:
        max_direction = max(best_dir_score[index_pos])
        index_max_direction = best_dir_score[index_pos].index(max_direction)

    # défini l'index de la position avec le plus de scores
    max_position = max(best_pos_score[index_pos][index_max_direction])
    index_max_position = best_pos_score[index_pos][index_max_direction].index(max_position)

    # déplace le pion
    position_pion_deplace_y = best_pos[index_pos][index_max_direction][index_max_position][0]
    position_pion_deplace_x = best_pos[index_pos][index_max_direction][index_max_position][1]
    plateau[position_pion_deplace_y][position_pion_deplace_x] = 'o'

    return index_max_direction, index_max_position


def ia_train(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other):
    plateau = creer_plateau(len_plateau)
    placer_pion(plateau)

    joueur = "expert"
    ia = "ia"
    main_joueur = joueur

    all_play = []  # Créer un nouveau tableau pour chaque jeu

    while cherche_pos_x(plateau) != 0 or cherche_pos_y(plateau) != 0:
        tmp_pos_y = cherche_pos_y(plateau)
        tmp_pos_x = cherche_pos_x(plateau)

        main_joueur = change_joueur(main_joueur, joueur, ia)
        if main_joueur == joueur:
            robot_deplace_pion_expert(plateau)
        elif main_joueur == ia:
            index_max_direction, index_max_position = ia_deplace_pion(plateau, best_pos, best_pos_score, best_dir_score)

            index_pos = concatener(tmp_pos_y, tmp_pos_x)
            all_play.append(index_pos)
            all_play.append(index_max_direction)
            all_play.append(index_max_position)

    i = 0

    if main_joueur == joueur:
        nb_win_other += 1
        for i in range(0, len(all_play), 3):
            index_to_update = all_play[i + 1]
            best_dir_score[all_play[i]][index_to_update] -= 1
            best_pos_score[all_play[i]][index_to_update][all_play[i + 2]] -= 1
    else:
        nb_win_ia += 1
        for i in range(0, len(all_play), 3):
            best_dir_score[all_play[i]][all_play[i + 1]] += 3
            best_pos_score[all_play[i]][all_play[i + 1]][all_play[i + 2]] += 3


    return nb_win_ia, nb_win_other



def ia_train_aicj(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other):
    plateau = creer_plateau(len_plateau)
    placer_pion(plateau)

    joueur = "joueur"
    ia = "ia"
    main_joueur = ia

    all_play = []  # Créer un nouveau tableau pour chaque jeu

    while cherche_pos_x(plateau) != 0 or cherche_pos_y(plateau) != 0:
        tmp_pos_y = cherche_pos_y(plateau)
        tmp_pos_x = cherche_pos_x(plateau)

        main_joueur = change_joueur(main_joueur, joueur, ia)

        print(main_joueur," joue !")

        affiche_plateau(plateau)
        if main_joueur == joueur:
            deplace_pion(plateau)
        elif main_joueur == ia:
            index_max_direction, index_max_position = ia_deplace_pion(plateau, best_pos, best_pos_score, best_dir_score)

            index_pos = concatener(tmp_pos_y, tmp_pos_x)
            all_play.append(index_pos)
            all_play.append(index_max_direction)
            all_play.append(index_max_position)

    i = 0

    if main_joueur == joueur:
        nb_win_other += 1
        for i in range(0, len(all_play), 3):
            index_to_update = all_play[i + 1]
            best_dir_score[all_play[i]][index_to_update] -= 1
            best_pos_score[all_play[i]][index_to_update][all_play[i + 2]] -= 1
    else:
        nb_win_ia += 1
        for i in range(0, len(all_play), 3):
            best_dir_score[all_play[i]][all_play[i + 1]] += 3
            best_pos_score[all_play[i]][all_play[i + 1]][all_play[i + 2]] += 3

    print("\n", main_joueur, "a Gagné la partie !")

    return nb_win_ia, nb_win_other


def ia_train_aicalea(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other):
    plateau = creer_plateau(len_plateau)
    placer_pion(plateau)

    joueur = "aleatoire"
    ia = "ia"
    main_joueur = ia

    all_play = []  # Créer un nouveau tableau pour chaque jeu

    while cherche_pos_x(plateau) != 0 or cherche_pos_y(plateau) != 0:
        tmp_pos_y = cherche_pos_y(plateau)
        tmp_pos_x = cherche_pos_x(plateau)

        main_joueur = change_joueur(main_joueur, joueur, ia)
        if main_joueur == joueur:
            robot_deplace_pion_alea(plateau)
        elif main_joueur == ia:
            index_max_direction, index_max_position = ia_deplace_pion(plateau, best_pos, best_pos_score, best_dir_score)

            index_pos = concatener(tmp_pos_y, tmp_pos_x)
            all_play.append(index_pos)
            all_play.append(index_max_direction)
            all_play.append(index_max_position)

    i = 0

    if main_joueur == joueur:
        nb_win_other += 1
        for i in range(0, len(all_play), 3):
            index_to_update = all_play[i + 1]
            best_dir_score[all_play[i]][index_to_update] -= 1
            best_pos_score[all_play[i]][index_to_update][all_play[i + 2]] -= 1
    else:
        nb_win_ia += 1
        for i in range(0, len(all_play), 3):
            best_dir_score[all_play[i]][all_play[i + 1]] += 3
            best_pos_score[all_play[i]][all_play[i + 1]][all_play[i + 2]] += 3

    return nb_win_ia, nb_win_other




def ia_train_aicai(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other):
    plateau = creer_plateau(len_plateau)
    placer_pion(plateau)

    joueur = "ia2"
    ia = "ia"
    main_joueur = joueur

    all_play = []  # Créer un nouveau tableau pour chaque jeu

    while cherche_pos_x(plateau) != 0 or cherche_pos_y(plateau) != 0:
        tmp_pos_y = cherche_pos_y(plateau)
        tmp_pos_x = cherche_pos_x(plateau)

        main_joueur = change_joueur(main_joueur, joueur, ia)
        if main_joueur == joueur:
            index_max_direction, index_max_position = ia_deplace_pion(plateau, best_pos, best_pos_score, best_dir_score)
        elif main_joueur == ia:
            index_max_direction, index_max_position = ia_deplace_pion(plateau, best_pos, best_pos_score, best_dir_score)

            index_pos = concatener(tmp_pos_y, tmp_pos_x)
            all_play.append(index_pos)
            all_play.append(index_max_direction)
            all_play.append(index_max_position)

    i = 0

    if main_joueur == joueur:
        nb_win_other += 1
        for i in range(0, len(all_play), 3):
            index_to_update = all_play[i + 1]
            best_dir_score[all_play[i]][index_to_update] -= 1
            best_pos_score[all_play[i]][index_to_update][all_play[i + 2]] -= 1
    else:
        nb_win_ia += 1
        for i in range(0, len(all_play), 3):
            best_dir_score[all_play[i]][all_play[i + 1]] += 3
            best_pos_score[all_play[i]][all_play[i + 1]][all_play[i + 2]] += 3

    return nb_win_ia, nb_win_other




### Game

def main():
    """ 
    présentation de l'IA

    """

    skip = 0
    while skip != 1 and skip != 2:
        skip = int(input("skip l'introduction ? :\n\n\t 1- Oui\n\t 2- Non\n\n\t Choisir : "))
    if skip == 2:
        print("\n\n===================\n= Introduction IA =\n===================")

        print("Pour le TP de la Ressource R1.13 (Coloration IA), ", "nous avons dû créer une IA en Machine Learning pour jouer au jeu de Wythoff.")

        time.sleep(7)
        print("\nD'abord nous avons coder un environnement du jeu de Wythoff avec par exemple l'affichage du plateau ou des fonctions de déplacement pour que nous puissions jouer en joueur contre joueur.")

        time.sleep(9)
        print("\nSeulement nous devions encore créer l'IA, et nous savions déjà qu'entraîner l'IA manuellement allait être beaucoup trop long... C'est pourquoi avant de développer l'IA nous avons programmé 2 robot d'entrainement :")
        print("\t - Un robot jouant de manière aléatoire\n\t - Un deuxième robot expert jouant les meilleurs coups possible")

        time.sleep(15)
        print("\n\nMaintenant que notre environnement de jeu et nos robots d'entrainement sont prêt il ne nous restait plus qu'à créer notre IA.")

        time.sleep(7)
        print("\n\n=====================\n= Fonctionnement IA =\n=====================\n\n\t Pour que notre IA apprenne il fallait qu'elle puisse déterminé les meilleurs coups au fil des parties et qu'elle les retienne pour pouvoir s'y rendre dans le futur.")

        time.sleep(10)
        print("\n\n\t Nous avons alors eu l'idée de représenter sa mémoire par un tableau où chaque élément représentant un score pour chaque positions accessible à partir de chacune des positions du plateau.")
        print("\n\t Pour obtenir ce tableau nous commençons par créer un tableau des positions du plateau, puis créons un deuxième tableau de toutes les directions possible à partir de chaque position du plateau\n\t et enfin nous créons un tableau de toutes les positions accessible à partir de chaque directions de chaque positions du plateau")
        print("\n\t Après nous recopions simplement les 2 tableaux de directions et de positions puis nous remplaçons chaque élément par un score initialiser de base à 0.")

        time.sleep(25)
        print("\n\n\t En bref nous définissons un score pour chaque positions accessible à partir de chacune des positions du plateau.")

        time.sleep(7)
        print("\n\n\t Ces tableaux de scores sont la mémoire de l'IA, et pour qu'elle soit active, l'IA enregistre tous les coups qu'elle joue pour chacune de ses parties.")

        time.sleep(14)
        print("\n\n\t Dans le cas où elle gagne, tous les coups qu'elle a joué ont 3 de scores suplémentaire, cependant si elle perd tous les coups joué perdent 1 point de score.")
        print("\n\t Quand elle joue, l'IA se rend sytématiquement sur la position ayant le plus de points et à force de faire des parties elle finit par déterminer les meilleurs déplacements pour chaque positions du plateau.")

        time.sleep(15)
    print("\n\n=====================\n=    Example IA     =\n=====================")


    len_plateau = 10
    pos_init = creer_positions_initiales(len_plateau)

    best_pos = creer_best_position(pos_init)
    best_dir = creer_best_direction(pos_init)
    
    stop = False
    while stop == False:

        mode = 0
        while (mode != 1 and mode != 2 and mode != 3 and mode != 4 and mode != 5):
            time.sleep(0.5)
            mode = int(input("\n\n\tMode d'example :\n\n\tManuel\n\t 1- IA contre Joueur\n\t 2- IA contre Expert\n\t 3- IA contre Aléatoire\n\t 4- IA contre IA\n\n\tAutomatique\n\t 5- Full Auto\n\n\t Choisir : "))

        if mode != 5:
            time.sleep(0.5)
            typeAI = 0
            while (typeAI != 1) and (typeAI != 2):
                typeAI = int(input("\n\n\t IA déjà entraînée 1h30 Contre Robot Expert:\n\n\t 1- Oui\n\t 2- Non\n\n\t Choisir : "))
            time.sleep(0.5)
            
            nbGame = int(input("\n\n\t Nombre de partie souhaité :\n\n\t Choisir : "))

            if typeAI == 1:
                best_pos_score = [[[], [], []], [[151611], [], []], [[-1, 101223], [], []], [[-1, -1, 10545], [], []], [[-1, -1, -1, 3327], [], []], [[0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0, 0, 0, 0], [], []], [[], [148044], []], [[-1], [-1], [100260]], [[-3633, -3632], [-7264], [-7264]], [[22508, 0, 0], [0], [0]], [[-1, 15753, 0, 0], [-1], [-1]], [[-1, -1, 11778, 0, 0], [-2], [-2]], [[-1, -1, -1, 12201, 0, 0], [-3], [-3]], [[-1, -1, -1, -1, 12180, 0, 0], [-4], [-4]], [[-1, -1, -1, -1, -1, 11892, 0, 0], [-5], [-5]], [[-1, -1, -1, -1, -1, -1, 12213, 0, 0], [-6], [-6]], [[], [-1, 116328], []], [[-7849], [-3924, -3924], [-7848]], [[0, 0], [0, 0], [0, 0]], [[-1, 0, 0], [-1, 0], [23013, 0]], [[-1, -1, 15351, 0], [-1, -1], [-1, -1]], [[-1, -1, -1, 12285, 0], [-2, -1], [-2, -1]], [[-1, -1, -1, -1, 12066, 0], [-2, -2], [-2, -2]], [[-1, -1, -1, -1, -1, 12159, 0], [-3, -2], [-3, -2]], [[-1, -1, -1, -1, -1, -1, 11643, 0], [-3, -3], [-3, -3]], [[-1, -1, -1, -1, -1, -1, -1, 11742, 0], [-4, -3], [-4, -3]], [[], [-1, -1, 6150], []], [[-4], [29543, -1, -1], [-3]], [[-1, -1], [-1, 12378, 0], [-1, 0]], [[-1, -1, -1], [-1, -1, -1], [-1, -1, 10767]], [[-1, -1, 0, 0], [-1, -1, 0], [-1, 15534, 0]], [[-387, -387, -386, -386, -386], [-644, -644, -644], [-644, -644, -643]], [[-313, -313, -313, -312, -312, -312], [-625, -625, -625], [-625, -625, -624]], [[-243, -243, -243, -243, -243, -243, -242], [-567, -567, -566], [-567, -566, -566]], [[-214, -214, -214, -214, -213, -213, -213, -213], [-570, -569, -569], [-570, -569, -569]], [[-172, -172, -172, -172, -172, -172, -171, -171, -171], [-515, -515, -514], [-515, -515, -514]], [[], [0, 0, 0, 0], []], [[-2], [-1, 17916, 0, 0], [-1]], [[-2, -1], [-1, -1, 30336, 0], [-1, -1]], [[-1, -1, 0], [-1, -1, 0, 0], [-1, 22542, 0]], [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, 3378]], [[-1, -1, -1, 0, 0], [-1, -1, -1, 0], [-1, -1, 12450, 0]], [[-266, -265, -265, -265, -265, -265], [-398, -398, -398, -397], [-398, -398, -397, -397]], [[-219, -219, -219, -219, -218, -218, -218], [-383, -383, -382, -382], [-383, -382, -382, -382]], [[-185, -185, -185, -185, -184, -184, -184, -184], [-369, -369, -369, -368], [-369, -369, -369, -368]], [[-161, -161, -161, -161, -161, -161, -161, -161, -161], [-362, -362, -362, -362], [-362, -362, -362, -362]], [[], [-1, -1, -1, -1, 17595], []], [[-3], [-1, -1, 30093, 0, 0], [-2]], [[-2, -2], [-1, -1, -1, 35853, 0], [-2, -1]], [[-813, -813, -812], [-488, -488, -487, -487, -487], [-813, -812, -812]], [[-1, -1, -1, 0], [-1, -1, -1, 0, 0], [-1, -1, 15375, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[-1, -1, 12192, 0, 0, 0], [-1, -1, 0, 0, 0], [-1, -1, 0, 0, 0]], [[-2, -2, -2, 12068, -1, -1, -1], [-2, -2, -2, -2, -2], [-2, -2, -2, -2, -2]], [[-1, -1, -1, -1, 12576, 0, 0, 0], [-1, -1, -1, -1, 0], [-1, -1, -1, -1, 0]], [[-1, -1, -1, -1, -1, 11980, 0, 0, 0], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], [[], [0, 0, 0, 0, 0, 0], []], [[-4], [-1, -1, -1, 11997, 0, 0], [-3]], [[-3, -2], [-1, -1, -1, -1, 12162, 0], [-2, -2]], [[-1, 0, 0], [18108, 0, 0, 0, 0, 0], [0, 0, 0]], [[-1, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [15538, 0, 0, 0]], [[-1, -1, -1, -1, 0], [-1, -1, -1, -1, 0, 0], [-1, -1, -1, 11970, 0]], [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], [[-1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, 11997, 0]], [[-173, -173, -173, -173, -173, -173, -173, -172], [-231, -231, -230, -230, -230, -230], [-231, -231, -230, -230, -230, -230]], [[-150, -150, -150, -150, -150, -150, -149, -149, -149], [-225, -225, -224, -224, -224, -224], [-225, -225, -224, -224, -224, -224]], [[], [-1, -1, -1, -1, -1, -1, 5841], []], [[-5], [-1, -1, -1, -1, 17988, 0, 0], [-4]], [[-3, -3], [-1, -1, -1, -1, -1, 17946, 0], [-3, -2]], [[-3, -3, -3], [-2, 18305, -1, -1, -1, -1, -1], [-3, -3, -2]], [[-401, -401, -400, -400], [-229, -229, -229, -229, -229, -228, -228], [-401, -400, -400, -400]], [[-1, -1, 0, 0, 0], [-1, -1, 0, 0, 0, 0, 0], [-1, 11947, 0, 0, 0]], [[-1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, 11868, 0]], [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[-1, -1, -1, 11772, 0, 0, 0, 0], [-1, -1, -1, 0, 0, 0, 0], [-1, -1, -1, 0, 0, 0, 0]], [[-2, -2, -2, -2, 12331, -1, -1, -1, -1], [-2, -2, -2, -2, -2, -2, -1], [-2, -2, -2, -2, -2, -2, -1]], [[], [0, 0, 0, 0, 0, 0, 0, 0], []], [[-6], [-1, -1, -1, -1, -1, 12264, 0, 0], [-5]], [[-4, -3], [-1, -1, -1, -1, -1, -1, 11949, 0], [-3, -3]], [[-4, -4, -3], [-2, -2, 11906, -1, -1, -1, -1, -1], [-4, -3, -3]], [[-3, -2, -2, -2], [11997, -1, -1, -1, -1, -1, -1, -1], [-2, -2, -2, -2]], [[-3, -2, -2, -2, -2], [-2, -2, -2, -1, -1, -1, -1, -1], [11997, -2, -2, -2, -2]], [[-2, -2, -2, -1, -1, -1], [-2, -1, -1, -1, -1, -1, -1, -1], [-2, -2, 11930, -1, -1, -1]], [[-1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, 12171, 0]], [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], [[-1, -1, -1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, 11967, 0]], [[], [0, 0, 0, 0, 0, 0, 0, 0, 0], []], [[-7], [-1, -1, -1, -1, -1, -1, 12066, 0, 0], [-6]], [[-4, -4], [-1, -1, -1, -1, -1, -1, -1, 12045, 0], [-4, -3]], [[-2, -1, -1], [-1, -1, -1, 12155, 0, 0, 0, 0, 0], [-1, -1, -1]], [[-3, -3, -3, -2], [-2, 11830, -1, -1, -1, -1, -1, -1, -1], [-3, -3, -2, -2]], [[-268, -268, -268, -268, -268], [-149, -149, -149, -149, -149, -149, -149, -149, -148], [-268, -268, -268, -268, -268]], [[-1, -1, 0, 0, 0, 0], [-1, -1, 0, 0, 0, 0, 0, 0, 0], [-1, 12044, 0, 0, 0, 0]], [[-1, -1, -1, -1, 0, 0, 0], [-1, -1, -1, -1, 0, 0, 0, 0, 0], [-1, -1, -1, 11895, 0, 0, 0]], [[-1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, -1, 12198, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]]
                best_dir_score = [[0, 0, 0], [151611, 0, 0], [101222, 0, 0], [10543, 0, 0], [3324, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 148044, 0], [-1, -1, 100260], [-7265, -7264, -7264], [22508, 0, 0], [15752, -1, -1], [11776, -2, -2], [12198, -3, -3], [12176, -4, -4], [11887, -5, -5], [12207, -6, -6], [0, 116327, 0], [-7849, -7848, -7848], [0, 0, 0], [-1, -1, 23013], [15349, -2, -2], [12282, -3, -3], [12062, -4, -4], [12154, -5, -5], [11637, -6, -6], [11735, -7, -7], [0, 6148, 0], [-4, 29541, -3], [-2, 12377, -1], [-3, -3, 10765], [-2, -2, 15533], [-1932, -1932, -1931], [-1875, -1875, -1874], [-1700, -1700, -1699], [-1708, -1708, -1708], [-1545, -1544, -1544], [0, 0, 0], [-2, 17915, -1], [-3, 30334, -2], [-2, -2, 22541], [-4, -4, 3375], [-3, -3, 12448], [-1591, -1591, -1590], [-1530, -1530, -1529], [-1476, -1475, -1475], [-1449, -1448, -1448], [0, 17591, 0], [-3, 30091, -2], [-4, 35850, -3], [-2438, -2437, -2437], [-3, -3, 15373], [0, 0, 0], [12190, -2, -2], [12059, -10, -10], [12572, -4, -4], [11975, -5, -5], [0, 0, 0], [-4, 11994, -3], [-5, 12158, -4], [-1, 18108, 0], [-1, -1, 15538], [-4, -4, 11967], [0, 0, 0], [-5, -5, 11993], [-1383, -1382, -1382], [-1347, -1346, -1346], [0, 5835, 0], [-5, 17984, -4], [-6, 17941, -5], [-9, 18298, -8], [-1602, -1601, -1601], [-2, -2, 11946], [-5, -5, 11864], [0, 0, 0], [11769, -3, -3], [12319, -13, -13], [0, 0, 0], [-6, 12259, -5], [-7, 11943, -6], [-11, 11897, -10], [-9, 11990, -8], [-11, -11, 11989], [-9, -9, 11923], [-6, -6, 12166], [0, 0, 0], [-7, -7, 11961], [0, 0, 0], [-7, 12060, -6], [-8, 12038, -7], [-4, 12152, -3], [-11, 11821, -10], [-1340, -1340, -1340], [-2, -2, 12043], [-4, -4, 11892], [-7, -7, 12192], [0, 0, 0]]
            
            else:
                best_dir_score = creer_best_direction_score(best_dir)
                best_pos_score = creer_best_position_score(best_pos)


            
            nb_win_ia = 0
            nb_win_other = 0

            curr = time.time()
            
            if mode == 1:
                for i in range(nbGame):
                    nb_win_ia, nb_win_other = ia_train_aicj(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other)
            
            elif mode == 2:
                for i in range(nbGame):
                    nb_win_ia, nb_win_other = ia_train(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other)
                

            elif mode == 3:
                for i in range(nbGame):
                    nb_win_ia, nb_win_other = ia_train_aicalea(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other)
            
            elif mode == 4:
                for i in range(nbGame):
                    nb_win_ia, nb_win_other = ia_train_aicai(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other)
            
            finish = time.time()

            timer = finish - curr

            time.sleep(3)
            print("\n\nTableau des scores des directions :\n",best_dir_score,"\n\n")
            time.sleep(3)
            print("\n\nTableau des scores des positions :\n",best_pos_score,"\n\n")

            time.sleep(3)
            print("nombre win ia : ",nb_win_ia)
            print("nombre win other : ",nb_win_other)
            print("Temps : ", timer)
        
        else:
            print("\n\n=====================\n=     Mode Auto     =\n=====================")
            i = 1
            while i < 3:
                j = 1
                while j <= 4:
                    if i == 1:
                        time.sleep(2)
                        print("\n\n=====================\n= IA Non Entrainée  =\n=====================")

                        best_dir_score = creer_best_direction_score(best_dir)
                        best_pos_score = creer_best_position_score(best_pos)
                    else:
                        time.sleep(2)
                        print("\n\n=====================\n=   IA Entrainée    =\n=====================")
                        best_pos_score = [[[], [], []], [[151611], [], []], [[-1, 101223], [], []], [[-1, -1, 10545], [], []], [[-1, -1, -1, 3327], [], []], [[0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0, 0, 0, 0], [], []], [[], [148044], []], [[-1], [-1], [100260]], [[-3633, -3632], [-7264], [-7264]], [[22508, 0, 0], [0], [0]], [[-1, 15753, 0, 0], [-1], [-1]], [[-1, -1, 11778, 0, 0], [-2], [-2]], [[-1, -1, -1, 12201, 0, 0], [-3], [-3]], [[-1, -1, -1, -1, 12180, 0, 0], [-4], [-4]], [[-1, -1, -1, -1, -1, 11892, 0, 0], [-5], [-5]], [[-1, -1, -1, -1, -1, -1, 12213, 0, 0], [-6], [-6]], [[], [-1, 116328], []], [[-7849], [-3924, -3924], [-7848]], [[0, 0], [0, 0], [0, 0]], [[-1, 0, 0], [-1, 0], [23013, 0]], [[-1, -1, 15351, 0], [-1, -1], [-1, -1]], [[-1, -1, -1, 12285, 0], [-2, -1], [-2, -1]], [[-1, -1, -1, -1, 12066, 0], [-2, -2], [-2, -2]], [[-1, -1, -1, -1, -1, 12159, 0], [-3, -2], [-3, -2]], [[-1, -1, -1, -1, -1, -1, 11643, 0], [-3, -3], [-3, -3]], [[-1, -1, -1, -1, -1, -1, -1, 11742, 0], [-4, -3], [-4, -3]], [[], [-1, -1, 6150], []], [[-4], [29543, -1, -1], [-3]], [[-1, -1], [-1, 12378, 0], [-1, 0]], [[-1, -1, -1], [-1, -1, -1], [-1, -1, 10767]], [[-1, -1, 0, 0], [-1, -1, 0], [-1, 15534, 0]], [[-387, -387, -386, -386, -386], [-644, -644, -644], [-644, -644, -643]], [[-313, -313, -313, -312, -312, -312], [-625, -625, -625], [-625, -625, -624]], [[-243, -243, -243, -243, -243, -243, -242], [-567, -567, -566], [-567, -566, -566]], [[-214, -214, -214, -214, -213, -213, -213, -213], [-570, -569, -569], [-570, -569, -569]], [[-172, -172, -172, -172, -172, -172, -171, -171, -171], [-515, -515, -514], [-515, -515, -514]], [[], [0, 0, 0, 0], []], [[-2], [-1, 17916, 0, 0], [-1]], [[-2, -1], [-1, -1, 30336, 0], [-1, -1]], [[-1, -1, 0], [-1, -1, 0, 0], [-1, 22542, 0]], [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, 3378]], [[-1, -1, -1, 0, 0], [-1, -1, -1, 0], [-1, -1, 12450, 0]], [[-266, -265, -265, -265, -265, -265], [-398, -398, -398, -397], [-398, -398, -397, -397]], [[-219, -219, -219, -219, -218, -218, -218], [-383, -383, -382, -382], [-383, -382, -382, -382]], [[-185, -185, -185, -185, -184, -184, -184, -184], [-369, -369, -369, -368], [-369, -369, -369, -368]], [[-161, -161, -161, -161, -161, -161, -161, -161, -161], [-362, -362, -362, -362], [-362, -362, -362, -362]], [[], [-1, -1, -1, -1, 17595], []], [[-3], [-1, -1, 30093, 0, 0], [-2]], [[-2, -2], [-1, -1, -1, 35853, 0], [-2, -1]], [[-813, -813, -812], [-488, -488, -487, -487, -487], [-813, -812, -812]], [[-1, -1, -1, 0], [-1, -1, -1, 0, 0], [-1, -1, 15375, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[-1, -1, 12192, 0, 0, 0], [-1, -1, 0, 0, 0], [-1, -1, 0, 0, 0]], [[-2, -2, -2, 12068, -1, -1, -1], [-2, -2, -2, -2, -2], [-2, -2, -2, -2, -2]], [[-1, -1, -1, -1, 12576, 0, 0, 0], [-1, -1, -1, -1, 0], [-1, -1, -1, -1, 0]], [[-1, -1, -1, -1, -1, 11980, 0, 0, 0], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], [[], [0, 0, 0, 0, 0, 0], []], [[-4], [-1, -1, -1, 11997, 0, 0], [-3]], [[-3, -2], [-1, -1, -1, -1, 12162, 0], [-2, -2]], [[-1, 0, 0], [18108, 0, 0, 0, 0, 0], [0, 0, 0]], [[-1, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [15538, 0, 0, 0]], [[-1, -1, -1, -1, 0], [-1, -1, -1, -1, 0, 0], [-1, -1, -1, 11970, 0]], [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], [[-1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, 11997, 0]], [[-173, -173, -173, -173, -173, -173, -173, -172], [-231, -231, -230, -230, -230, -230], [-231, -231, -230, -230, -230, -230]], [[-150, -150, -150, -150, -150, -150, -149, -149, -149], [-225, -225, -224, -224, -224, -224], [-225, -225, -224, -224, -224, -224]], [[], [-1, -1, -1, -1, -1, -1, 5841], []], [[-5], [-1, -1, -1, -1, 17988, 0, 0], [-4]], [[-3, -3], [-1, -1, -1, -1, -1, 17946, 0], [-3, -2]], [[-3, -3, -3], [-2, 18305, -1, -1, -1, -1, -1], [-3, -3, -2]], [[-401, -401, -400, -400], [-229, -229, -229, -229, -229, -228, -228], [-401, -400, -400, -400]], [[-1, -1, 0, 0, 0], [-1, -1, 0, 0, 0, 0, 0], [-1, 11947, 0, 0, 0]], [[-1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, 11868, 0]], [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[-1, -1, -1, 11772, 0, 0, 0, 0], [-1, -1, -1, 0, 0, 0, 0], [-1, -1, -1, 0, 0, 0, 0]], [[-2, -2, -2, -2, 12331, -1, -1, -1, -1], [-2, -2, -2, -2, -2, -2, -1], [-2, -2, -2, -2, -2, -2, -1]], [[], [0, 0, 0, 0, 0, 0, 0, 0], []], [[-6], [-1, -1, -1, -1, -1, 12264, 0, 0], [-5]], [[-4, -3], [-1, -1, -1, -1, -1, -1, 11949, 0], [-3, -3]], [[-4, -4, -3], [-2, -2, 11906, -1, -1, -1, -1, -1], [-4, -3, -3]], [[-3, -2, -2, -2], [11997, -1, -1, -1, -1, -1, -1, -1], [-2, -2, -2, -2]], [[-3, -2, -2, -2, -2], [-2, -2, -2, -1, -1, -1, -1, -1], [11997, -2, -2, -2, -2]], [[-2, -2, -2, -1, -1, -1], [-2, -1, -1, -1, -1, -1, -1, -1], [-2, -2, 11930, -1, -1, -1]], [[-1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, 12171, 0]], [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], [[-1, -1, -1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, 11967, 0]], [[], [0, 0, 0, 0, 0, 0, 0, 0, 0], []], [[-7], [-1, -1, -1, -1, -1, -1, 12066, 0, 0], [-6]], [[-4, -4], [-1, -1, -1, -1, -1, -1, -1, 12045, 0], [-4, -3]], [[-2, -1, -1], [-1, -1, -1, 12155, 0, 0, 0, 0, 0], [-1, -1, -1]], [[-3, -3, -3, -2], [-2, 11830, -1, -1, -1, -1, -1, -1, -1], [-3, -3, -2, -2]], [[-268, -268, -268, -268, -268], [-149, -149, -149, -149, -149, -149, -149, -149, -148], [-268, -268, -268, -268, -268]], [[-1, -1, 0, 0, 0, 0], [-1, -1, 0, 0, 0, 0, 0, 0, 0], [-1, 12044, 0, 0, 0, 0]], [[-1, -1, -1, -1, 0, 0, 0], [-1, -1, -1, -1, 0, 0, 0, 0, 0], [-1, -1, -1, 11895, 0, 0, 0]], [[-1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, -1, 12198, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]]
                        best_dir_score = [[0, 0, 0], [151611, 0, 0], [101222, 0, 0], [10543, 0, 0], [3324, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 148044, 0], [-1, -1, 100260], [-7265, -7264, -7264], [22508, 0, 0], [15752, -1, -1], [11776, -2, -2], [12198, -3, -3], [12176, -4, -4], [11887, -5, -5], [12207, -6, -6], [0, 116327, 0], [-7849, -7848, -7848], [0, 0, 0], [-1, -1, 23013], [15349, -2, -2], [12282, -3, -3], [12062, -4, -4], [12154, -5, -5], [11637, -6, -6], [11735, -7, -7], [0, 6148, 0], [-4, 29541, -3], [-2, 12377, -1], [-3, -3, 10765], [-2, -2, 15533], [-1932, -1932, -1931], [-1875, -1875, -1874], [-1700, -1700, -1699], [-1708, -1708, -1708], [-1545, -1544, -1544], [0, 0, 0], [-2, 17915, -1], [-3, 30334, -2], [-2, -2, 22541], [-4, -4, 3375], [-3, -3, 12448], [-1591, -1591, -1590], [-1530, -1530, -1529], [-1476, -1475, -1475], [-1449, -1448, -1448], [0, 17591, 0], [-3, 30091, -2], [-4, 35850, -3], [-2438, -2437, -2437], [-3, -3, 15373], [0, 0, 0], [12190, -2, -2], [12059, -10, -10], [12572, -4, -4], [11975, -5, -5], [0, 0, 0], [-4, 11994, -3], [-5, 12158, -4], [-1, 18108, 0], [-1, -1, 15538], [-4, -4, 11967], [0, 0, 0], [-5, -5, 11993], [-1383, -1382, -1382], [-1347, -1346, -1346], [0, 5835, 0], [-5, 17984, -4], [-6, 17941, -5], [-9, 18298, -8], [-1602, -1601, -1601], [-2, -2, 11946], [-5, -5, 11864], [0, 0, 0], [11769, -3, -3], [12319, -13, -13], [0, 0, 0], [-6, 12259, -5], [-7, 11943, -6], [-11, 11897, -10], [-9, 11990, -8], [-11, -11, 11989], [-9, -9, 11923], [-6, -6, 12166], [0, 0, 0], [-7, -7, 11961], [0, 0, 0], [-7, 12060, -6], [-8, 12038, -7], [-4, 12152, -3], [-11, 11821, -10], [-1340, -1340, -1340], [-2, -2, 12043], [-4, -4, 11892], [-7, -7, 12192], [0, 0, 0]]

                    nb_win_ia = 0
                    nb_win_other = 0

                    curr = time.time()
                    
                    if j == 1:
                        time.sleep(2)
                        print("\n\nIA CONTRE JOUEUR => 1 Game :\n\n")
                        time.sleep(4)
                        for k in range(1):
                            nb_win_ia, nb_win_other = ia_train_aicj(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other)
                    
                    elif j == 2:
                        time.sleep(2)
                        print("\n\nIA CONTRE EXPERT => 10 000 Games :\n\n")
                        time.sleep(4)
                        for k in range(10000):
                            nb_win_ia, nb_win_other = ia_train(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other)
                        

                    elif j == 3:
                        time.sleep(2)
                        print("\n\nIA CONTRE ALEATOIRE => 10 000 Games :\n\n")
                        time.sleep(4)
                        for k in range(10000):
                            nb_win_ia, nb_win_other = ia_train_aicalea(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other)
                    
                    elif j == 4:
                        time.sleep(2)
                        print("\n\nIA CONTRE IA => 10 000 Games :\n\n")
                        time.sleep(4)
                        for k in range(10000):
                            nb_win_ia, nb_win_other = ia_train_aicai(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other)
                    
                    finish = time.time()

                    timer = finish - curr

                    time.sleep(3)
                    print("\n\nTableau des scores des directions :\n",best_dir_score,"\n\n")
                    time.sleep(3)
                    print("\n\nTableau des scores des positions :\n",best_pos_score,"\n\n")

                    time.sleep(3)
                    print("nombre win ia : ",nb_win_ia)
                    print("nombre win other : ",nb_win_other)
                    print("Temps : ", timer)

                    j = j + 1
                
                i = i + 1

        cont = 0
        while (cont != 1) and (cont != 2):
            cont = int(input("\n\n\t Voulez vous continuez les examples ?\n\n\t 1- Oui\n\t 2- Non\n\n\t Choisir : "))
        if cont == 2:
            stop = True
            print("\n\n Le programme va s'arrêté, si vous voulez entrainer l'IA vous même et comme vous le souhaitez, vous pouvez utilisé la fonction play()")
            time.sleep(3)
        


        

def play():
    """ mentrainement de l'ia

    Args:
        plateau (tab[][]): plateau où le jeu se déroule
    """
    len_plateau = 10
    pos_init = creer_positions_initiales(len_plateau)

    best_pos = creer_best_position(pos_init)
    best_dir = creer_best_direction(pos_init)

    print(best_dir)

    #ia entrainer 1h30 contre expert
    #best_pos_score = [[[], [], []], [[151611], [], []], [[-1, 101223], [], []], [[-1, -1, 10545], [], []], [[-1, -1, -1, 3327], [], []], [[0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0, 0, 0], [], []], [[0, 0, 0, 0, 0, 0, 0, 0, 0], [], []], [[], [148044], []], [[-1], [-1], [100260]], [[-3633, -3632], [-7264], [-7264]], [[22508, 0, 0], [0], [0]], [[-1, 15753, 0, 0], [-1], [-1]], [[-1, -1, 11778, 0, 0], [-2], [-2]], [[-1, -1, -1, 12201, 0, 0], [-3], [-3]], [[-1, -1, -1, -1, 12180, 0, 0], [-4], [-4]], [[-1, -1, -1, -1, -1, 11892, 0, 0], [-5], [-5]], [[-1, -1, -1, -1, -1, -1, 12213, 0, 0], [-6], [-6]], [[], [-1, 116328], []], [[-7849], [-3924, -3924], [-7848]], [[0, 0], [0, 0], [0, 0]], [[-1, 0, 0], [-1, 0], [23013, 0]], [[-1, -1, 15351, 0], [-1, -1], [-1, -1]], [[-1, -1, -1, 12285, 0], [-2, -1], [-2, -1]], [[-1, -1, -1, -1, 12066, 0], [-2, -2], [-2, -2]], [[-1, -1, -1, -1, -1, 12159, 0], [-3, -2], [-3, -2]], [[-1, -1, -1, -1, -1, -1, 11643, 0], [-3, -3], [-3, -3]], [[-1, -1, -1, -1, -1, -1, -1, 11742, 0], [-4, -3], [-4, -3]], [[], [-1, -1, 6150], []], [[-4], [29543, -1, -1], [-3]], [[-1, -1], [-1, 12378, 0], [-1, 0]], [[-1, -1, -1], [-1, -1, -1], [-1, -1, 10767]], [[-1, -1, 0, 0], [-1, -1, 0], [-1, 15534, 0]], [[-387, -387, -386, -386, -386], [-644, -644, -644], [-644, -644, -643]], [[-313, -313, -313, -312, -312, -312], [-625, -625, -625], [-625, -625, -624]], [[-243, -243, -243, -243, -243, -243, -242], [-567, -567, -566], [-567, -566, -566]], [[-214, -214, -214, -214, -213, -213, -213, -213], [-570, -569, -569], [-570, -569, -569]], [[-172, -172, -172, -172, -172, -172, -171, -171, -171], [-515, -515, -514], [-515, -515, -514]], [[], [0, 0, 0, 0], []], [[-2], [-1, 17916, 0, 0], [-1]], [[-2, -1], [-1, -1, 30336, 0], [-1, -1]], [[-1, -1, 0], [-1, -1, 0, 0], [-1, 22542, 0]], [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, 3378]], [[-1, -1, -1, 0, 0], [-1, -1, -1, 0], [-1, -1, 12450, 0]], [[-266, -265, -265, -265, -265, -265], [-398, -398, -398, -397], [-398, -398, -397, -397]], [[-219, -219, -219, -219, -218, -218, -218], [-383, -383, -382, -382], [-383, -382, -382, -382]], [[-185, -185, -185, -185, -184, -184, -184, -184], [-369, -369, -369, -368], [-369, -369, -369, -368]], [[-161, -161, -161, -161, -161, -161, -161, -161, -161], [-362, -362, -362, -362], [-362, -362, -362, -362]], [[], [-1, -1, -1, -1, 17595], []], [[-3], [-1, -1, 30093, 0, 0], [-2]], [[-2, -2], [-1, -1, -1, 35853, 0], [-2, -1]], [[-813, -813, -812], [-488, -488, -487, -487, -487], [-813, -812, -812]], [[-1, -1, -1, 0], [-1, -1, -1, 0, 0], [-1, -1, 15375, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[-1, -1, 12192, 0, 0, 0], [-1, -1, 0, 0, 0], [-1, -1, 0, 0, 0]], [[-2, -2, -2, 12068, -1, -1, -1], [-2, -2, -2, -2, -2], [-2, -2, -2, -2, -2]], [[-1, -1, -1, -1, 12576, 0, 0, 0], [-1, -1, -1, -1, 0], [-1, -1, -1, -1, 0]], [[-1, -1, -1, -1, -1, 11980, 0, 0, 0], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], [[], [0, 0, 0, 0, 0, 0], []], [[-4], [-1, -1, -1, 11997, 0, 0], [-3]], [[-3, -2], [-1, -1, -1, -1, 12162, 0], [-2, -2]], [[-1, 0, 0], [18108, 0, 0, 0, 0, 0], [0, 0, 0]], [[-1, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [15538, 0, 0, 0]], [[-1, -1, -1, -1, 0], [-1, -1, -1, -1, 0, 0], [-1, -1, -1, 11970, 0]], [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], [[-1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, 11997, 0]], [[-173, -173, -173, -173, -173, -173, -173, -172], [-231, -231, -230, -230, -230, -230], [-231, -231, -230, -230, -230, -230]], [[-150, -150, -150, -150, -150, -150, -149, -149, -149], [-225, -225, -224, -224, -224, -224], [-225, -225, -224, -224, -224, -224]], [[], [-1, -1, -1, -1, -1, -1, 5841], []], [[-5], [-1, -1, -1, -1, 17988, 0, 0], [-4]], [[-3, -3], [-1, -1, -1, -1, -1, 17946, 0], [-3, -2]], [[-3, -3, -3], [-2, 18305, -1, -1, -1, -1, -1], [-3, -3, -2]], [[-401, -401, -400, -400], [-229, -229, -229, -229, -229, -228, -228], [-401, -400, -400, -400]], [[-1, -1, 0, 0, 0], [-1, -1, 0, 0, 0, 0, 0], [-1, 11947, 0, 0, 0]], [[-1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, 11868, 0]], [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[-1, -1, -1, 11772, 0, 0, 0, 0], [-1, -1, -1, 0, 0, 0, 0], [-1, -1, -1, 0, 0, 0, 0]], [[-2, -2, -2, -2, 12331, -1, -1, -1, -1], [-2, -2, -2, -2, -2, -2, -1], [-2, -2, -2, -2, -2, -2, -1]], [[], [0, 0, 0, 0, 0, 0, 0, 0], []], [[-6], [-1, -1, -1, -1, -1, 12264, 0, 0], [-5]], [[-4, -3], [-1, -1, -1, -1, -1, -1, 11949, 0], [-3, -3]], [[-4, -4, -3], [-2, -2, 11906, -1, -1, -1, -1, -1], [-4, -3, -3]], [[-3, -2, -2, -2], [11997, -1, -1, -1, -1, -1, -1, -1], [-2, -2, -2, -2]], [[-3, -2, -2, -2, -2], [-2, -2, -2, -1, -1, -1, -1, -1], [11997, -2, -2, -2, -2]], [[-2, -2, -2, -1, -1, -1], [-2, -1, -1, -1, -1, -1, -1, -1], [-2, -2, 11930, -1, -1, -1]], [[-1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, 12171, 0]], [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], [[-1, -1, -1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, 11967, 0]], [[], [0, 0, 0, 0, 0, 0, 0, 0, 0], []], [[-7], [-1, -1, -1, -1, -1, -1, 12066, 0, 0], [-6]], [[-4, -4], [-1, -1, -1, -1, -1, -1, -1, 12045, 0], [-4, -3]], [[-2, -1, -1], [-1, -1, -1, 12155, 0, 0, 0, 0, 0], [-1, -1, -1]], [[-3, -3, -3, -2], [-2, 11830, -1, -1, -1, -1, -1, -1, -1], [-3, -3, -2, -2]], [[-268, -268, -268, -268, -268], [-149, -149, -149, -149, -149, -149, -149, -149, -148], [-268, -268, -268, -268, -268]], [[-1, -1, 0, 0, 0, 0], [-1, -1, 0, 0, 0, 0, 0, 0, 0], [-1, 12044, 0, 0, 0, 0]], [[-1, -1, -1, -1, 0, 0, 0], [-1, -1, -1, -1, 0, 0, 0, 0, 0], [-1, -1, -1, 11895, 0, 0, 0]], [[-1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, 0, 0], [-1, -1, -1, -1, -1, -1, 12198, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]]
    #best_dir_score = [[0, 0, 0], [151611, 0, 0], [101222, 0, 0], [10543, 0, 0], [3324, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 148044, 0], [-1, -1, 100260], [-7265, -7264, -7264], [22508, 0, 0], [15752, -1, -1], [11776, -2, -2], [12198, -3, -3], [12176, -4, -4], [11887, -5, -5], [12207, -6, -6], [0, 116327, 0], [-7849, -7848, -7848], [0, 0, 0], [-1, -1, 23013], [15349, -2, -2], [12282, -3, -3], [12062, -4, -4], [12154, -5, -5], [11637, -6, -6], [11735, -7, -7], [0, 6148, 0], [-4, 29541, -3], [-2, 12377, -1], [-3, -3, 10765], [-2, -2, 15533], [-1932, -1932, -1931], [-1875, -1875, -1874], [-1700, -1700, -1699], [-1708, -1708, -1708], [-1545, -1544, -1544], [0, 0, 0], [-2, 17915, -1], [-3, 30334, -2], [-2, -2, 22541], [-4, -4, 3375], [-3, -3, 12448], [-1591, -1591, -1590], [-1530, -1530, -1529], [-1476, -1475, -1475], [-1449, -1448, -1448], [0, 17591, 0], [-3, 30091, -2], [-4, 35850, -3], [-2438, -2437, -2437], [-3, -3, 15373], [0, 0, 0], [12190, -2, -2], [12059, -10, -10], [12572, -4, -4], [11975, -5, -5], [0, 0, 0], [-4, 11994, -3], [-5, 12158, -4], [-1, 18108, 0], [-1, -1, 15538], [-4, -4, 11967], [0, 0, 0], [-5, -5, 11993], [-1383, -1382, -1382], [-1347, -1346, -1346], [0, 5835, 0], [-5, 17984, -4], [-6, 17941, -5], [-9, 18298, -8], [-1602, -1601, -1601], [-2, -2, 11946], [-5, -5, 11864], [0, 0, 0], [11769, -3, -3], [12319, -13, -13], [0, 0, 0], [-6, 12259, -5], [-7, 11943, -6], [-11, 11897, -10], [-9, 11990, -8], [-11, -11, 11989], [-9, -9, 11923], [-6, -6, 12166], [0, 0, 0], [-7, -7, 11961], [0, 0, 0], [-7, 12060, -6], [-8, 12038, -7], [-4, 12152, -3], [-11, 11821, -10], [-1340, -1340, -1340], [-2, -2, 12043], [-4, -4, 11892], [-7, -7, 12192], [0, 0, 0]]

    best_dir_score = creer_best_direction_score(best_dir)
    best_pos_score = creer_best_position_score(best_pos)

    nb_win_ia = 0
    nb_win_other = 0

    curr = time.time()

    for i in range(1000000):
        nb_win_ia, nb_win_other = ia_train(len_plateau, best_pos, best_pos_score, best_dir_score, nb_win_ia, nb_win_other)
        print(best_dir_score,"\n\n")
        print(best_pos_score,"\n\n")

    finish = time.time()

    timer = finish - curr

    print("best dir score\n",best_dir_score,"\n\n")
    print("best pos score\n",best_pos_score,"\n\n")
    
    print("nombre win ia : ",nb_win_ia)
    print("nombre win other : ",nb_win_other)

    print("Temps : ", timer)

    finish = True
    while finish:
        choice = int(input("choisis le mode : "))
        if choice == 0:
            finish = False
        elif choice == 1:
            jeu_joueur_contre_ia(best_pos, best_pos_score, best_dir_score)


main()


