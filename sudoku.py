from copy import deepcopy

N = None
grille_facile = [
    [N,N,N, 4,N,7, N,5,8],
    [N,N,7, N,1,5, N,3,2],
    [N,N,4, 6,N,3, N,N,N],

    [N,N,N, 1,3,N, 8,6,N],
    [N,N,N, N,N,N, 1,N,N],
    [N,N,N, 5,9,8, N,N,N],

    [8,9,N, N,5,6, 7,4,3],
    [7,2,N, 3,N,9, N,8,1],
    [N,N,5, 8,N,1, 2,9,N]]

grille_moyenne =  [
    [N,N,N, N,N,N, 4,N,2],
    [6,N,N, 7,N,N, N,1,N],
    [5,N,N, N,2,N, 7,N,N],

    [N,3,N, N,1,N, N,4,8],
    [N,4,N, 2,N,N, N,N,N],
    [N,8,N, 9,N,N, N,5,N],

    [N,5,N, N,N,3, N,7,N],
    [N,N,N, N,N,N, N,N,N],
    [9,N,N, 1,N,N, N,8,N]]

grille_difficile =  [
    [N,N,N, N,N,6, N,N,N],
    [1,N,N, N,N,N, N,3,N],
    [N,N,2, 9,7,N, 8,N,N],

    [2,N,N, 6,4,N, N,N,1],
    [N,N,N, N,N,5, 4,N,N],
    [N,N,6, N,N,8, N,N,N],

    [N,7,N, N,N,N, N,N,8],
    [N,N,N, N,5,N, N,N,N],
    [N,N,9, 4,2,N, 7,N,N]]

def print_grille(g):
    """jolie affichage d'une grille"""
    C = deepcopy(g)
    for c in range(len(C)) : 
        for case in range(len(C[c])) : 
            if C[c][case]==None : C[c][case] = " "
    for i in range (9) : 
        if i%3 ==0 and i!=0 : 
            print("|___|___|___")
        for j in range (9) : 
            if j%3==0 : print('|', end="")
            print(C[i][j], end="")
        print("")
print_grille(grille_moyenne)
 
def complet (g) : 
    for col in g : 
        for case in col : 
            if case==None : return False
    return True

def case_min (g) : 
    min = (9, None)
    for i in range (9) : 
        for j in range (9) : 
            if g[i][j]==None and len(min[0])>len(g[i][j]) : min = (g[i][j], (i, j))
    return min

def colonne(g, j, pos) : 
    for i in range(9) : 
        #print(g[i][j], pos)
        if g[i][j] in pos : pos.remove(g[i][j])
    return pos

def ligne(g, i, pos) : 
    for j in range(9) : 
        #print(g[i][j], pos)
        if g[i][j] in pos : pos.remove(g[i][j])
    return pos

def bloc (g, i, j, pos) : 
    for k in range (3*(i//3), 3*(i//3+1)) : 
        for l in range (3*(j//3), 3*(j//3+1)) : 
            #print(g[i][j], pos)
            if g[k][l] in pos : pos.remove(g[k][l])
    return pos

def possible(g,i,j):
    """donne la liste des valeurs possibles pour la case (i,j) de la grille g.
       tient uniquement compte des valeurs présentes dans la même ligne,
       colonne ou bloc."""
    pos = [i for i in range(1, 10)]
    pos = colonne(g, j, pos)
    pos = ligne(g, i, pos)
    pos = bloc(g, i, j, pos)
    return pos

print(possible(grille_facile, 3, 5))

def possibles(g):
    """return un tableau de taille 9x9, avec dans la case (i,j)
       - None si la case est remplie dans la grille g,
       - la liste des valeurs possibles sinon."""
    sudo = [[] for i in range (9)]
    for i in range (9) : 
        for j in range (9) : 
            s = possible(g, i, j)
            if g[i][j]!=None : sudo[i].append(None)
            else : 
                sudo[i].append(s)
    return sudo

def realisable(g):
    sudok = possibles(g)
    for col in sudok : 
        if [] in col : return False
    return True

print(possibles(grille_facile))

def SAT_sol (sudok) : 
    if complet(sudok)==True : return sudok
    case = case_min(sudok)[1]
    pos = case_min(sudok)[0]
    grille  = deepcopy(sudok)
    grille[case[0]][case[1]] = pos[0]
    if 
    


def resoud_possible(g):
    """résoud une grille de sudoku en prenant une case à la fois"""
    iterations = 0
    added = 0
    while iterations<1000 and complet(g)!=True : 
        print(added)
        added = 0
        s = []
        for i in range (9) : 
            for j in range (9) : 
                if g[i][j] == None : 
                    s = possible(g, i, j)
                    if len(s)==1 : 
                        g[i][j] = s[0]
                        added+=1
        iterations+=1
    print_grille(g)

def resoud_possibles(g) : 
    """résoud une grille de sudoku en faisant la totalité des cases"""
    iterations = 0
    added = 0
    while iterations<1000 and complet(g)!=True : 
        added = 0
        sudo = possibles(g)
        for i in range(9) : 
            for j in range (9) : 
                if sudo[i][j]!=None : 
                    if len(sudo[i][j])==1 : 
                        g[i][j] = sudo[i][j][0]
                        added+=1
                        print(added)
        if added == 0 : 
        iterations+=1
    print_grille(g)
resoud_possibles(grille_moyenne)