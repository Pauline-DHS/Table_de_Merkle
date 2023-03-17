# Projet : Contrôle d'intégrité de données avec l'arbre de Merkle

# Contexte
Ce projet a pour objectif d'expérimenter le contrôle d'intégrité de données en utilisant l'arbre de Merkle. Nous allons utiliser l'implémentation de la fonction de hachage TTH5-64.

Les arbres de Merkle permettent un contrôle d'intégrité d'un ensemble de données (par exemple, un fichier) sur la base d'une possession partielle. Ce projet va nous permettre de le vérifier.

# Contrôle d'intégrité
Le contrôle d'intégrité "cryptographique" suppose l'utilisation d'une fonction de hachage cryptographique. Ainsi, en connaissant la valeur 0xBB3C associée à DATA, nous pouvons contrôler son intégrité en calculant TTH5-64(DATA) = 0xBB3C.

# Partitionnement en blocs
DATA peut également être considérée comme une concaténation de blocs de données. Nous proposerons une implantation d'un tel partitionnement à partir d'un fichier, en considérant des blocs de 512 octets. Dans le cas où la taille du fichier à partitionner n'est pas multiple de 512, nous procéderons, comme nous avons vu en TP, au bourrage du dernier bloc à 512 en utilisant le vecteur 10000000...00000. Bien entendu, la reconstruction de DATA suppose, le cas échéant, le débourrage de ce dernier bloc.

# Contrôle d'intégrité par parties en possédant toutes les parties
Le contrôle d'intégrité par parties permet, à partir du partitionnement en blocs de 512 octets de DATA, de réaliser de la même façon qu'avant un contrôle d'intégrité global de DATA. Cela peut être réalisé en construisant un arbre de Merkle. Nous implémenterons le module qui calcule la racine de l'arbre de Merkle pour DATA en utilisant notre brique logicielle TTH5-64.

# Contrôle d'intégrité global pour une partie
Si l'on suppose que l'on ne considère qu'une seule partie de DATA, il est toujours possible de réaliser un contrôle d'intégrité global de l'information en ne considérant qu'une quantité d'informations supplémentaire d'ordre logarithmique correspondant aux empreintes "alternatives" allant de la feuille à la racine de l'arbre.

