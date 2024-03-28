import copy as cp


class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """
    
    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
            réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """
        
        # alphabet
        alphabet = list("abcdefghijklmnopqrstuvwxyzEO")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in alphabet:
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            self.n = 0
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")" 
        
    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k,v in self.transition.items():    
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res
    
    def ajoute_transition(self, q0, a, qlist):
        """ajoute la liste de transitions (q0, a, q1) pour tout q1 dans qlist à l'automate"""
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})
    
    
def concatenation(a1, a2): 
    """Retourne l'automate qui reconnaît la concaténation des 
    langages reconnus par les automates a1 et a2"""
    
    # on copie pour éviter les effets de bord     
    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)
    res = automate()
    # les états finals sont ceux de a2 dont les identifiants sont décalés de a1.n
    res.final = [(i + a1.n) for i in a2.final]
    res.name = "(" + a1.name + "." + a2.name + ")"
    # on ajoute les transitions de a1 et a2 en mettant à jour les identifiants
    for k,v in a1.transition.items():
        res.ajoute_transition(*k, v)    
    for k,v in a2.transition.items():
        res.ajoute_transition(k[0] + a1.n, k[1],  [e+a1.n for e in v])
    # on ajoute les epsilon transitions
    for i in a1.final:
        res.ajoute_transition(i, "E", [a1.n])
    # on met à jour la taille de l'automate
    res.n = a1.n + a2.n
    return res


def union(a1, a2):
    """Retourne l'automate qui reconnaît l'union des 
    langages reconnus par les automates a1 et a2""" 
    
    # on copie pour éviter les effets de bord     
    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)
    res = automate()
    # les états finals avec le décalage idoine
    res.final = [(i + 1) for i in a1.final] + [(i + 1 + a1.n) for i in a2.final]
    res.name = "(" + a1.name + "+" + a2.name + ")"
    # on ajoute les transitions de a1 et a2 en mettant à jour les identifiants
    for k,v in a1.transition.items():
        res.ajoute_transition(k[0] + 1, k[1],  [e+1 for e in v])
    for k,v in a2.transition.items():
        res.ajoute_transition(k[0] + 1 + a1.n, k[1],  [e+1+a1.n for e in v])   
    # on ajoute les epsilon transition
    res.ajoute_transition(0, "E", [1])
    res.ajoute_transition(0, "E", [1 + a1.n])
    # on met à jour la taille de l'automate
    res.n = a1.n + a2.n + 1
    return res


def etoile(a):
    """Retourne l'automate qui reconnaît l'étoile de Kleene du 
    langage reconnu par l'automate a""" 
    
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.final = a.final
    res.transition = a.transition
    # on ajoute les epsilon transition
    for i in res.final:
        res.ajoute_transition(i, "E", [0])
    res.n = a.n
    # on calcule l'automate union avec l'automate epsilon
    res = union(res, automate("E"))
    res.name = a.name + "*"
    return res


def acces_epsilon(a):
    """ retourne la liste pour chaque état des états accessibles par epsilon transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    res = dict()
    for i in range(a.n):
        for k, v in a.transition.items():
            if k[0] == i and k[1] == 'E':
                res.update({i: v})
    # regarde l'entiereté des chemins avec des epsilons
    for k in cp.deepcopy(res).keys():
        copy = res.get(k)
        for elem in copy:
            for k1, v1 in a.transition.items():
                if k1[0] == elem and k1[1] == 'E':
                    temp = res.get(k)
                    for elem in cp.deepcopy(v1):
                        temp.append(elem)
                    res.update({k: list(set(temp))})
    return res

def suppression_epsilon(a):
    """ retourne l'automate sans les espilon transitions
    """
    eps = acces_epsilon(a)
    for _ in range(len(eps)):
        # pour chaque epsilon
        for etat, arrivé in eps.items():
            for arrive_epsilon in arrivé:
                for (etat_depart, lettre), v in cp.deepcopy(a).transition.items():
                    if lettre != 'E' and arrive_epsilon == etat_depart:
                        # si il y a deja une transition on ajoute à la suite
                        if a.transition.get((etat, lettre)):
                            temp = a.transition.get((etat, lettre))
                            temp.append(v[0])
                            a.transition.update({(etat, lettre): list(set(temp))})
                        else:
                            a.transition.update({(etat, lettre): v})
                    # ajout des nouveaux états finaux
                if arrive_epsilon in a.final and etat not in a.final:
                    a.final.append(etat)
    # supprime les epsilon de la liste
    for transi, v in cp.deepcopy(a).transition.items():
        if transi[1] == 'E':
            a.transition.pop(transi)
    return a

def determinisation(a):
    nb_etat = a.n
    etat = []
    taille = 1
    for i in a.transition.values():
        taille = max(len(i), taille)
    for i in range(taille):
        copy = cp.deepcopy(a)
        for k, v in copy.transition.items():
            # si l'état n'est pas déterminiser
            if len(v) > 1:
                etat.append(v) if v not in etat else None
                number = nb_etat + etat.index(v)
                a.n += 1
                a.transition.update({(k[0], k[1]): [number]})
                for k2, v2 in cp.deepcopy(a).transition.items():
                    for liste_elem in etat:
                        for elem in liste_elem:
                            if elem == k2[0]:
                                a.transition.update({(number, k2[1]): v2})
                # ajout etats final
                for elem in etat:
                    for val in elem:
                        if val in a.final:
                            a.final.append(number)
        a.final = list(set(a.final))
    return a
            

def reconnait(a, mot):
    """ Renvoie vrai si le mot mot est reconnu par l'automate a
    """
    if mot == "O" and 0 in a.final:
        return True
    etat = 0
    taille_mot = len(mot)
    cpt = 0
    for lettre in mot:
        if lettre == "E" :  
            cpt +=1
        else :
            for k, v in a.transition.items():
                if k[0] == etat and lettre == k[1]:
                    etat = v[0]
                    cpt +=1
                    break
                else:
                    continue
    if etat in a.final and taille_mot == cpt:
        return True
    else:
        return False


# TESTS
if __name__ == "__main__":
    # (a)
    a1 = automate("b")
    print(a1)
    # (b)
    a2 = automate("a")
    print(a2)
    # (ab)
    a3 = concatenation(a1, a2)
    print(a3)
    # (a+b)
    a4 = union(a1, a2)
    print(a4)
    # a*
    a5 = etoile(a2)
    print(a5)
    # a** (pour tester epsilon-transitions accessibilité avec circuit)
    a6 = etoile(a5)
    print(a6)
    print(acces_epsilon(a6))
    # tests de reconnaissance 
    print(reconnait(a5, "aaa"))
    print(reconnait(a5, "aab"))
    print(reconnait(a6, "aaa"))
    print(reconnait(a6, "aab"))