

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
    print(blocks_bits)
    # Si nécessaire ajout du padding
    if padding != 6: 
        blocks_bits[indice_dernier_block] += '1'
        for i in range(padding-1):
            blocks_bits[indice_dernier_block] += '0'
    print(blocks_bits)
    # Convertion de chaque blocs de bit en valeur décimal
    blocks = []
    for block in blocks_bits:
        blocks.append(binary2decimal64(block))
        
    return blocks

def Padding(M):
    # Calcul du padding à ajouter pour avoir des gros blocs de 25
    padding = 25 - len(M) % 25
    print(len(M))
    # Si nécessaire ajout du padding
    if padding != 25: 
        M.append(32)
        for i in range(padding-1):
            M.append(00)
    print(M)
    return M

def ArrangementMatriciel(M_dec):
    # Stocker les tableaux générés dans une liste
    tableaux = []
    cpt = 0
    # Arrangement matriciel de M+padding
    nb_block = int(len(M_dec) / 25)
    print(len(M_dec))
    print(nb_block)
    for i in range(nb_block):
        # Générer un tableau avec des éléments allant de 0 à i
        tableau = [[0 for j in range(5)] for i in range(5)]
        for i in range(5):
            for j in range(5):
                tableau[i][j] = M_dec[cpt]
                cpt += 1
        tableaux.append(tableau)
        for ligne in tableau:
            print(ligne,"\n")
        print('--------------------------')
    
    return tableaux

def CalculBlocEtape1(tableau,Empreinte):
    
    # ETAPE 1 -> EMPREINTE
    
    for ligne in tableau:
            Empreinte[0] += ligne[0]
            Empreinte[1] += ligne[1]
            Empreinte[2] += ligne[2]
            Empreinte[3] += ligne[3]
            Empreinte[4] += ligne[4]
    
    for i in range(len(Empreinte)-1):
        Empreinte[i] = (Empreinte[i]-(int(Empreinte[i] / 64))*64)
    print(Empreinte)
    print('--------------------------')

    return Empreinte

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
    for ligne in tableau:
        print(ligne,"\n")
    print('--------------------------')
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
    
    for tableau in tableaux:
        print("NOVEAU TABLEAU")
        Empreinte = CalculBlocEtape1(tableau,Empreinte)
        tableau = CalculBlocEtape2(tableau)
        Empreinte = CalculBlocEtape1(tableau,Empreinte)
    


# Message clair sous forme binaire
M = "10010101010101010100101010101010110011101010100101010101000000111110010011010110101010101101010101010101011001010101010101010010101010101010011100101010010101010100000011111001001101011010101010110101010101010101101101010101010101010100110101010010101010101011111010001001010010010101010101010101001101010100101010101010111110100010010100100"
TTH564(M)

#?########################################################################################################
#?--------------------------------------------------------------------------------------------------------
#?########################################################################################################

import struct
def ParitionnementEnBlocsBinaire4096(file):
    file_binary = ""
    taille = 0
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
    while i < nb_block:
        block = file_binary[(4096*i):((4096*i)+4096)]
        tableaux_data.append(block)
        print(block)
        print(len(block))
        print("\n------------------------\n")
        i +=1


ParitionnementEnBlocsBinaire4096("file.txt")