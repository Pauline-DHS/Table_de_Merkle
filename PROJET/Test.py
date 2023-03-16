with open('file.txt', 'rb') as f_binaire:
    # Lire les données binaires du fichier binaire
    donnees_binaires = f_binaire.read()
    
    # Convertir les données binaires en chaîne de caractères de 0 et de 1
    donnees_binaires_string = binascii.hexlify(donnees_binaires).decode('utf-8')
    
    # Afficher les données binaires sous forme de chaîne de 0 et de 1
    print(donnees_binaires_string)