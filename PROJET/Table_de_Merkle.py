
#?########################################################################################################
#?-----------------------------------------------------TTH564---------------------------------------------
#?########################################################################################################

# Cette fonction va permettre de convertir les blocs de bits en valeurs décimal
def binary2decimal64(binary):
    binary = int(binary)
    int_val, i, n = 0,0,0
    while(binary != 0):
        a = binary % 10
        int_val = int_val + a * pow(2,i)
        binary = binary//10
        i += 1
    return int_val

# Cette fonction va permettre de répartir le message en bloc de 6 bits ou moins pour pouvoir
# par la suite les convertir en valeur décimal inférieur ou égal à 64
def ConversionDec(M):
    blocks_bits = []
    for i in range(0, len(M), 6):
        block = M[i:i+6]
        blocks_bits.append(block)
    
    # Stock l'indice du dernière blocs 
    indice_dernier_block = len(blocks_bits)-1
    
    # Calcul du padding à ajouter sur le dernière bloc
    padding = 6 - len(blocks_bits[indice_dernier_block]) % 6
    
    # Si nécessaire ajout du padding
    if padding != 6: 
        blocks_bits[indice_dernier_block] += '1'
        for i in range(padding-1):
            blocks_bits[indice_dernier_block] += '0'
    
    # Convertion de chaque blocs de bit en valeur décimal
    blocks = []
    for block in blocks_bits:
        blocks.append(binary2decimal64(block))
        
    return blocks

# Cette fonction permet le bourrage des données pour obtenir un multiple de 25 
def Padding(M):
    # Calcul du padding à ajouter pour avoir des gros blocs de 25
    padding = 25 - len(M) % 25
    
    # Si nécessaire ajout du padding
    if padding != 25: 
        M.append(32)
        for i in range(padding-1):
            M.append(00)
    
    return M

# Cette fonction permet de créer des tableaux de 5x5 pour chaque blocs de données
def ArrangementMatriciel(M_dec):
    # Stocker les tableaux générés dans une liste
    tableaux = []
    cpt = 0
    # Arrangement matriciel de M+padding
    nb_block = int(len(M_dec) / 25)
    
    for i in range(nb_block):
        # Générer un tableau avec des éléments allant de 0 à i
        tableau = [[0 for j in range(5)] for i in range(5)]
        for i in range(5):
            for j in range(5):
                tableau[i][j] = M_dec[cpt]
                cpt += 1
        tableaux.append(tableau)
    
    return tableaux

# Cette fonction permet de calculer l'empreinte d'un bloc
def CalculBlocEtape1(tableau,Empreinte):
    
    # ETAPE 1 -> EMPREINTE
    # Calcul en colonne
    for ligne in tableau:
            Empreinte[0] += ligne[0]
            Empreinte[1] += ligne[1]
            Empreinte[2] += ligne[2]
            Empreinte[3] += ligne[3]
            Empreinte[4] += ligne[4]
    
    # Adaptation en décimal < à 64
    for i in range(len(Empreinte)):
        Empreinte[i] = (Empreinte[i]-(int(Empreinte[i] / 64))*64)

    return Empreinte

# Cette fonction permet d'effectuer le décalage nécessaire avant le calcul des empreintes de la fonction CalculBlocEtape1
def CalculBlocEtape2(tableau):
    
     # ETAPE 2 -> DECALAGE CIRCULAIRE
    i=4
    for index, line in enumerate(tableau):
        
        # si c'est la première ligne, on la saute
        if index == 0:  
            continue
        valeur_dec = line[i:]
        valeur_autre = line[:i]
        for val in valeur_autre:
            valeur_dec.append(val)
        line.clear()
        tableau[index] = valeur_dec
        i -= 1
    return tableau

# Cette fonction va permettre de hacher le message selon une fonction de hachage TTH564 inspiré 
# de la fonction TTH
def TTH564(M):
    
    Empreinte = [0,0,0,0,0]
    
    # Conversion en décimaldu message M
    M_dec = ConversionDec(M)
    
    # Padding du message M
    M_ = Padding(M_dec)
    
    # Arrangement Matriciel de M+Padding 
    # Création de matrice 5x5 contenant les valeurs décimales de M_
    tableaux = ArrangementMatriciel(M_)
    
    # Processus à suivre pour aboutir à une empreinte finale
    for tableau in tableaux:
        Empreinte = CalculBlocEtape1(tableau,Empreinte)
        tableau = CalculBlocEtape2(tableau)
        Empreinte = CalculBlocEtape1(tableau,Empreinte)
    
    # Mise en format chaine de l'empreinte
    result = ""
    for case in Empreinte:
        result += str(case)
    
    return result

#?########################################################################################################
#?-------------------------------------------------------ARBRE DE MERKLE-----------------------------------
#?########################################################################################################

import math
import struct

# Cette fonction va permettre de retranscrire le fichier au format binaire et de partionner le fichier en plusieurs blocs de données
def ParitionnementEnBlocsBinaire4096(file):
    file_binary = ""
    taille = 0
    
    # Ouvertur du fichier
    with open(file, 'rb') as f:
        byte = f.read(1)
        while byte:
            # Convertir l'octet en un entier non signé (unsigned int)
            num = struct.unpack('B', byte)[0]
            
            # Concaténer la représentation binaire de l'octet à la variable file_binary
            binary = bin(num)[2:].zfill(8)  
            taille += 1  
            file_binary += binary
            
            byte = f.read(1)

    taille *= 8
    # Calcul du padding à ajouter sur le dernière bloc
    padding = 4096 - taille  % 4096

    # Si nécessaire ajout du padding
    if padding != 4096: 
        file_binary += '1'
        taille += 1
        for i in range(padding-1):
            file_binary += '0'
            taille += 1
        
    # Stocker les tableaux générés dans une liste
    tableaux_data = []

    # Arrangement matriciel de M+padding
    nb_block = int(taille / 4096)

    block=[]
    i = 1
    
    # Division et stokage des différents bloc/tableau de 512 octets dans un tableau 
    while i < nb_block:
        block = file_binary[(4096*i):((4096*i)+4096)]
        tableaux_data.append(block)
        i +=1
    
    return tableaux_data

# Cette fonction permet de calculer toutes les empreintes de chaque bloc de données
def InitialiationFeuilleMerkle(blocs):
    global arbre
    tab_Emp = []
    # Pour chaque bloque => calcul de l'empreinte et ajout de celle-ci dans la liste à retourner
    for bloc in blocs:
        E1 = TTH564(bloc)
        tab_Emp.append(E1)
    # Stoke tous les blocs de données (utilisé dans la dernière partie du projet)
    arbre.append(blocs)
    return tab_Emp

def MerkleCalcul(tab_Emp):
    global arbre
    
    # Si il n'y a qu'un élément dans l'arbre => il s'agit de la racine
    if (len(tab_Emp) == 1):
        # Stoke toutes les empreintes de chaque couche (utilisé dans la dernière partie du projet)
        arbre.append(tab_Emp)
        return tab_Emp[0]
    
    i = 0
    tab_ = []
    
    # Stoke toutes les empreintes de chaque couche (utilisé dans la dernière partie du projet)
    arbre.append(tab_Emp)
    
    # Va boucler autant de fois qu'il y d'élément dans l'arbre
    for i in range(len(tab_Emp)):
        
        # Si ce n'est pas le dernier élément de la liste
        if i+1 < len(tab_Emp):
            # Concaténation des emprainte
            tmp = tab_Emp[i] + tab_Emp[i+1]
            # Fonction TTH564 renvoie une empreinte finale de cette nouvelles empreintes
            E1_E2 = TTH564(tmp)
             # Ajout de cette nouvelle empreinte dans une nouvelle liste
            tab_.append(E1_E2)
            
    # Appel récursif de la fonction avec la nouvelle liste
    return MerkleCalcul(tab_)


# Exécution de la table de Merkle sur le fichier
arbre = []
blocs = ParitionnementEnBlocsBinaire4096("file.txt")
racine = MerkleCalcul(InitialiationFeuilleMerkle(blocs))

#?########################################################################################################
#?---------------------------------------------ARBRE DE MERKLE GLOBAL------------------------------------#
#?########################################################################################################
#* CONTRÔLE D'INTEGRITE GLOBAL POUR UNE PARTIE 
# Cette fonction va permettre de calculer la racine selon la table de Merkle à partir d'un bloc de donnée et d'une liste
# qui contient le minimum d'empreinte nécessaire pour pouvoir la calculer
def Merkle2(arbre_know):
    global arbre_global
    
    # Si il n'y a qu'un élément dans l'arbre => il s'agit de la racine
    if len(arbre_know) == 1:
        arbre_global = arbre_know
        return arbre_know
    
    # Récupère les deux premiers éléments de notre listes d'empreintes
    couple = arbre_know[0]
    couple2 = arbre_know[1]
    
    # Si le numéro de la couche de nos deux empreintes est identique => on peut appliquer la fonction TTH564
    if couple[1] == couple2[1]:
        # Concatéation des empreintes
        tmp = couple[0] + couple2[0]
        # Fonction TTH564 renvoie une empreinte finale de cette nouvelles empreintes
        E1_E2 = TTH564(tmp)
        new_arbre = []
        # Ajout de cette nouvelle empreinte dans une nouvelle liste
        new_arbre.append((E1_E2,couple[1]+1))
        # Ajout de tous les éléments de la liste précédente dans la nouvelle à l'exception des deux premiers
        # qui ont été utilisé pour calculer la nouvelle empreinte déjà stokée
        for couple in arbre_know[2:]:
            new_arbre.append(couple)
        
        # Appel récursif de la fonction avec la nouvelle liste
        return Merkle2(new_arbre)

# Cette fonction permet de retourner l'indice du blocs dans la couche des feuilles ainsi que la hauteur de l'arbre
def IndexHauteur(arbre):
    # Récupère l'indice du bloc dans l'arbre
    index_DATA = 0
    for data in arbre[0]:
        if data == DATA:
            break
        index_DATA += 1
    return index_DATA, len(arbre)

# Récuperation des empreintes des blocs de données du fichier préalablement calculées
BLOCS = arbre[0] 

# Lancement de la nouvelle fonction pour chaque bloc de donnée indépendament des ordres
for DATA in BLOCS:
    # Arbre qui va contenir les empreintes que je dois obligatoirement connaitre pour faire le calul
    arbre_know = []

    # Récupère l'indice du bloc de donnée dans l'abre ainsi que la hauteur de celui ci
    index_DATA, HAUTEUR = IndexHauteur(arbre)
    
    print("Bloc n° : ",index_DATA)
    
    # Test si le bloc de donnée se situe sur le bord droit de l'arbre
    if (index_DATA == len(arbre[0])-1):
        # Si indice impaire
        if index_DATA % 2 != 0:
            # Pour chaque couche de mon arbre (sauf la première couche (data) et la dernière (racine))
            for i in range (2,HAUTEUR-1):
                # Récupère la couche
                couche = arbre[i]
                # Stocke chaque empreinte sur le bord droit de l'arbre dans un couple de données avec leur numéro de couche
                arbre_know.append((couche[index_DATA-i],i))
            # Stocke la première valeur (empreinte calculé avec le bloc de donnée qu'on veut tester) dans un couple de
            # données avec le numéro de sa couche
            arbre_know.insert(0,(TTH564(DATA),2))
            
        # Si indice paire
        else:
            j = 0
            # Pour chaque couche de mon arbre (sauf la dernière (racine))
            for i in range (1,HAUTEUR-1):
                # Récupère la couche
                couche = arbre[i]
                # Traitement spécial pour la première couche pour stocker l'empreinte de son voisin
                if i == 1:
                    j = 1
                # Stocke chaque empreinte sur le bord droit de l'arbre dans un couple de données avec leur numéro de couche
                arbre_know.append((couche[index_DATA-i-j],i))
            # Stocke la première valeur (empreinte calculé avec le bloc de donnée qu'on veut tester) dans un couple de
            # données avec le numéro de sa couche
            arbre_know.insert(0,(TTH564(DATA),1))
            
    # Test si le bloc de donnée se situe sur le bord gauche de l'arbre
    elif  (index_DATA == 0):
        # Pour chaque couche de mon arbre (sauf la dernière (racine))
        for i in range (1,HAUTEUR-1):
            # Récupère la couche
            couche = arbre[i]
            # Traitement spécial pour la première couche pour stocker l'empreinte de son voisin
            if i == 1:
                arbre_know.append((couche[index_DATA+i],i))
            # Stocke chaque empreinte sur le bord gauche de l'arbre dans un couple de données avec leur numéro de couche
            else:
                arbre_know.append((couche[0],i))
        # Stocke la première valeur (empreinte calculé avec le bloc de donnée qu'on veut tester) dans un couple de
        # données avec le numéro de sa couche
        arbre_know.insert(0,(TTH564(DATA),1))
    
    # Pour tous les autres blocs au centre
    elif (index_DATA % 2 == 0) or (index_DATA % 2 != 0):
        # Pour chaque couche de mon arbre (sauf la dernière (racine))
        for i in range(1,HAUTEUR-1):
            # Récupère la couche
            couche = arbre[i]
            # Traitement spécial pour la première couche pour stocker l'empreinte de son voisin
            if i == 1:
                arbre_know.append((couche[index_DATA+i],i))
             # Stocke chaque empreinte de l'arbre nécessaire pour le calcul dans un couple de données avec leur numéro de couche
            else:
                # Si indice du bloc en remontant dans les couches de l'arbre est pair
                if i % 2 == 0 and i < HAUTEUR:
                    # Calcul l'indice du voisin de droite du père de notre indice
                    index_DATA = math.ceil(index_DATA/2)
                    arbre_know.append((couche[index_DATA+1],i))
                # Si indice du bloc en remontant dans les couches de l'arbre est impaire
                else:
                    # Calcul l'indice du voisin de gauche du père de notre indice
                    index_DATA = math.ceil(index_DATA/2)
                    arbre_know.append((couche[index_DATA-1],i))
        # Stocke la première valeur (empreinte calculé avec le bloc de donnée qu'on veut tester) dans un couple de
        # données avec le numéro de sa couche
        arbre_know.insert(0,(TTH564(DATA),1))
        
    arbre_global = []
    Merkle2(arbre_know)
    
    # Vérification des deux racines (racine connue et racine calculée)
    if racine == arbre_global[0][0]:
        print("Intégrité vérifiée ✔️\n")
    else:
        print("Problème d'intégrité ❌\n")