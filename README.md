# Table_de_Merkle

Projet : Contrôle d'intégrité de données avec l'arbre de Merkle
1. Contexte
Ce projet a pour objectif d'expérimenter le contrôle d'intégrité de données en utilisant l'arbre de Merkle. Nous allons utiliser l'implémentation de la fonction de hachage TTH5-64 que nous avons réalisée lors des séances de TD. Cette implantation peut être faite dans le langage de notre choix, mais nous privilégierons les langages tels que C/C++, Python ou Java/Kotlin (langages propriétaires Windows proscrits).

Les arbres de Merkle permettent un contrôle d'intégrité d'un ensemble de données (par exemple, un fichier) sur la base d'une possession partielle. Ce projet va nous permettre de le vérifier.

1.1 Contrôle d'intégrité
Le contrôle d'intégrité "cryptographique" suppose l'utilisation d'une fonction de hachage cryptographique. Ainsi, en connaissant la valeur 0xBB3C associée à DATA, nous pouvons contrôler son intégrité en calculant TTH5-64(DATA) = 0xBB3C. Pour ce TP noté, DATA sera n'importe quel fichier de notre choix.

1.2 Partitionnement en blocs
DATA peut également être considérée comme une concaténation de blocs de données. Nous proposerons une implantation d'un tel partitionnement à partir d'un fichier, en considérant des blocs de 512 octets. Dans le cas où la taille du fichier à partitionner n'est pas multiple de 512, nous procéderons, comme nous avons vu en TP, au bourrage du dernier bloc à 512 en utilisant le vecteur 10000000...00000. Bien entendu, la reconstruction de DATA suppose, le cas échéant, le débourrage de ce dernier bloc.

1.3 Contrôle d'intégrité par parties en possédant toutes les parties
Le contrôle d'intégrité par parties permet, à partir du partitionnement en blocs de 512 octets de DATA, de réaliser de la même façon qu'avant un contrôle d'intégrité global de DATA. Cela peut être réalisé en construisant un arbre de Merkle. Nous implémenterons le module qui calcule la racine de l'arbre de Merkle pour DATA en utilisant notre brique logicielle TTH5-64.

1.4 Contrôle d'intégrité global pour une partie
Si l'on suppose que l'on ne considère qu'une seule partie de DATA, il est toujours possible de réaliser un contrôle d'intégrité global de l'information en ne considérant qu'une quantité d'informations supplémentaire d'ordre logarithmique correspondant aux empreintes "alternatives" allant de la feuille à la racine de l'arbre.

Nous proposerons une solution décrivant la façon dont nous intégrons les informations supplémentaires permettant le contrôle d'intégrité global pour chaque partie de DATA. Nous implémenterons ensuite les éléments que nous proposons à notre solution et écrirons la procédure de vérification du contrôle d'intégrité. Nous fournirons également un jeu de test pour nos solutions.
