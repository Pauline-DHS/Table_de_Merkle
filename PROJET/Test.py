class Noeud:
    def __init__(self, valeur, gauche=None, droit=None):
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit

    def est_feuille(self):
        return self.gauche is None and self.droit is None

    def __str__(self):
        return f"Noeud({self.valeur})"

class Feuille:
    def __init__(self, valeur):
        self.valeur = valeur

    def __str__(self):
        return f"Noeud({self.valeur})"

