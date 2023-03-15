#python

def TTH564(M):
    
    print("Taille du message M : ",len(M))
    
    # Padding du message M
    padding = 25 - len(M) % 25
    
    print("Valeur du padding calculé : ", padding)
    
    if padding != 25:
        M += '1' + '0' * (padding - 1) + '0' * (25 - padding)
        
    print("Message M : ",M)    
    print("Nouveau message M : ",M)    
    # Partitionnement en blocs de 25
    blocks = [M[i:i+25] for i in range(0, len(M), 25)]

    # Initialisation des valeurs d'empreinte
    h = [0, 0, 0, 0, 0]

    # Boucle de traitement des blocs
    for block in blocks:
        # Étape 1 : XOR des valeurs du bloc avec les valeurs d'empreinte
        for i in range(5):
            h[i] ^= int(block[i*5:i*5+5], 2)

        # Étape 2 : Permutation des valeurs d'empreinte
        h = [h[4]] + h[:4]

        # Étape 3 : Application d'une fonction non linéaire sur les valeurs d'empreinte
        h[0] = (h[0] << 1) | (h[0] >> 63)
        h[1] = (h[1] << 3) | (h[1] >> 61)
        h[2] = (h[2] << 6) | (h[2] >> 58)
        h[3] = (h[3] << 10) | (h[3] >> 54)
        h[4] = (h[4] << 15) | (h[4] >> 49)

        h[0] = h[0] ^ int(block, 2)

    return h

message = "1101010101101010101110101" # exemple de message binaire
empreinte = TTH564(message)
print(empreinte)
