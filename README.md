# shortest-path-3D
Deux fênetre se lancent lors de l'execution une avec tkinter terrain 2D
et une autre opengl avec le terrain en 3D
Sur l'application vous pouvez sélectionner plusieurs points et l'algorithme
de votre préference pour le calcul de plus court chemin, l'application OpenGL
devrait se mettre à jour en même temps que l'application 2D, ainsi que si les
dimensions du terrain.

Il est conseillé d'avoir les deux fênetres cote à cote car tous les 
préférences que vous chosirez sur l'application 2D se mettront à jour
sur l'application 3D.

## Choix d'implantation
### SortedDict
On a choisi de réaliser le plus court chemin à l'aide de un `sortedict` connu
sur le nom de map sur C++. Cela est dû à l'inexistence de une structure des 
données similiare en python de base.

### Tests unitaires
Sur le dossiers tests se situent tous les tests unitaires

