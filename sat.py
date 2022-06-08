
## Dans notre «sat solver», les variables sont des chaînes de caractères
## alpha numérique. La négation se note ``-``. Donc ``"-X"`` est la négation
## de ``"X"``. Par contre, la double négation nous ramène à la variable
## de départ (- par - ça fait +).

from copy import copy, deepcopy

def negation(v):
    """negation: ajoute un moins au début de la chaîne v si il n'y en a pas,
       l'enlève sinon"""
    return '-'+v if v[0]!='-' else v[1:]

assert negation("X") == "-X"
assert negation("-X") == "X"
assert negation("-X0") == "X0"

## On va d'abord évaluer les clauses et les problèmes si on nous donne
## une solution.

def valeur_clause(Cl,sol):
    """retourne True, si une des variables de Cl est dans sol"""
    for var in Cl : 
        if var in sol : return True
    return False

def valeur_pb(Pb,sol):
    """retourne True, si toutes les clauses de Pb sont satisfaites par sol"""
    for Cl in Pb : 
        if valeur_clause(Cl, sol) == False : return False 
    return True

pb1 = [["X"]]
pb2 = [["X"],["-X"]]
pb3 = [["X","Y"]]
pb4 = [["X","Y"],["-X","-Y"]]
pb5 = [["X","Y"],["-X","-Y"],["X","-Y", "Y"]]
pb6 = [["X","Y"],["-X","-Y"],["X","-Y"],["-X","Y"]]

assert valeur_pb(pb1,["X"])
assert not valeur_pb(pb2,["X"])
assert valeur_pb(pb3,["X"])
assert valeur_pb(pb4,["X","-Y"])
assert valeur_pb(pb5,["X","-Y"])
assert not valeur_pb(pb6,["X","-Y"])


## Une clause est une liste de variables ou de negation de variables.
## Pour qu'une clause soit vraie, il faut qu'une des variables soit vraie.
## Si on sait qu'une variable ``V`` est vraie, il est inutile de garder
## ``negation(V)`` dans une clause.

def enleve_negation(Cl,V):
    """ renvoie une copie de Cl (Cl n'est pas modifiée), où negation(V)
        a été enlevé, si elle apparaissait"""
    Clc = deepcopy(Cl)
    while negation(V) in Clc : Clc.remove(negation(V))
    return Clc

assert enleve_negation(["X","Y","Z"],"-Y") == ["X","Z"]
assert enleve_negation(["X","Y","Z"],"Y") == ["X","Y","Z"]

## Un problème est une liste de clauses. Pour satisfaire le problème,
## il faut trouver une valeur vraie ou fausse pour chaque variable pour
## que toutes les clauses soient vraies.

## Remarque: la clause vide est toujours fausse (elle ne contient aucune
## variable vraie) et le problème vide est toujours satisfait (toutes les
## clauses qu'il contient sont satisfaites).

## Si on sait qu'un variable ``V`` est vraie, toutes les clauses contenant
## V sont vraies et peuvent être enlevées du problèmes, et ``negation(V)``
## peut être enlevé des clauses restantes avec la fonction précédente.

def simplifie(Pb,V):
    """enlève de Pb les clauses contenant V et enlève negation(V) des autres
       clauses.  retourne le problème simplifié, sans modifier le problème
       original.
    """
    PbP = copy(Pb)
    for i in range(len(PbP)-1, -1, -1) : 
        #optimisation 2
        if V in PbP[i] and negation(V) in PbP[i] : 
            del PbP[i]
        elif negation(V) in PbP[i] : 
            #print('-')
            PbP[i]=enleve_negation(PbP[i],V)
        elif V in PbP[i] : PbP.remove(PbP[i])
    return PbP

## Pour résoudre un problème, à partir d'une solution partielle
## * si il est vide on retourne la solution
## * si il contient la clause vide on retourne ``False``
## * sinon, on prend une variable V dans le Pb, et on essaye
##   de résoudre avec ``V`` dans la solution ou avec ``negation(V)``
##   dans chaque cas, on ajoute ``V`` à la solution partielle et
##   on simplifie le problème.

def resoud_rec(Pb,sol):
    """ résoud un Pb avec une solution partielle. Si V est présent
        dans sol, ni V ni negation(V) ne doivent apparaître dans Pb."""
    if Pb == [] : return sol
    elif [] in Pb : return False
    V = Pb[0][0]
    sol2 = sol+[V]
    PbP = simplifie(Pb, V)
    #optimisation 1
    for Cl in Pb : 
        if len(Cl)==1 and Cl[0]!=V : 
            #on rajoute la variable de chaque clause univariable dans la solution
            sol2=sol2+Cl
            PbP=simplifie(PbP, Cl[0])
    if resoud_rec(PbP, sol2)==False: 
        sol2 = sol+[negation(V)]
        PbP = simplifie(Pb, negation(V))
    return resoud_rec(PbP, sol2)

## La fonction finale appelle simplement la précédente avec sol=[]
def resoud(Pb):
    """ résoud un problème Pb. renvoie False si il n'y a pas de solution,
        renvoie une solution sinon."""
    print(Pb)
    sol = resoud_rec(Pb,[])
    if sol: assert valeur_pb(Pb,sol)
    return(sol)

assert resoud(pb1) != False
assert resoud(pb2) == False
assert resoud(pb3) != False
assert resoud(pb4) != False
assert resoud(pb5) != False
assert resoud(pb6) == False

## Optimisation 1: que peut-on faire si le problème contient une clause
## avec une seule variable ? (good)

## Optimisation 2: est-il utile de garder une clause qui contient à la fois
## ``V`` et ``negation(V)`` (good)

## Tests: écrire une fonction qui génère des problèmes aléatoires grâce à la
## fonction ``randint(a,b)`` du module ``random`` qui donne un entier entre a
## et b inclus. Il suffit de générer ``M`` clauses de taille 3 en utilisant
## ``N`` variables pour que cela soit intéressant.

## Un problème ouvert: pour les 3-clauses aléatoires, il y a un seuil:
## * Si $M$ est plus petit que $S \times N$, le problème est très souvant résoluble.
## * Si $M$ est plus grand que $S \times N$, le problème n'a en général pas de solution.
## * Si $M = S \times N$, le problème est résoluble une fois sur deux.
## S est proche de 4.3, mais on ne connaît pas sa valeur exacte.
##
## Essayer de tracer une courbe proportion de problème résoluble en fonction
## de $M$
