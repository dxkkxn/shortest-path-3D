# shortest-path-3D
Au moment de l'exécution de ``main py`` deux fenêtres se lancent. Une sur Tkinter (terrain 2 D)
et une autre sur OpenGL avec le terrain en 3D.
Sur l'application Tkinter vous pouvez sélectionner plusieurs points et l'algorithme
de votre préférence afin de calculer le plus court chemin, l'application OpenGl
devrait se mettre à jour en même temps que l'application 2D, ainsi que les
dimensions du terrain.


Il est conseillé d'avoir les deux fenêtres côte à côte afin de profiter de la
mise à jour en temps réel des application 2D et 3D.


Sur l'application tkinter on peut choisir `(click gauche`) autant des points de controle que
vous voulez. Cependant pour avoir accés à certains paramètres on doit déselectionner
tous les points (`click droit`).

## Cahier des charges
- [x] codage, sauvegarde et chargement d’une matrice à valeurs entières, 
- [x] choix d’un point de départ et d’un point d’arrivée, application des algorithmes de Dijkstra et A* et mémorisation des résultats,
- [x] affichage de la matrice sous la forme d’un terrain en élévation,
- [x] déplacement d’un mobile le long de l’un des chemins trouvés au choix (de préférence sous la forme d’un ver, sinon modélisé par une simple sphère) dont les mouvements seront calculés par l’intermédiaire d’une succession de courbes de Bézier cubique,
- [x] ajout d’un obstacle infranchissable dans la génération du terrain et pris en compte par les algorithmes de recherche de chemin,
- [x] gestion d’une caméra offrant une vue générale et des mouvements en translation, rotation et zoom (sans utiliser glutSpaceball*),
- [x] représentation des obstacles infranchissables sous la forme de zones aquatiques (ou équivalents),
- [x] suivi du mouvement du mobile par la caméra durant son parcours du chemin,
- [x] application de textures (terrain et mobile).

La sauvegarde et le chargement n'ont pas mise en place car une solution plus 
élégante à été trouvé pour la communication entre les deux applications.
Et comme demandé lors d'un mail le seul interêt de faire cela était la 
communication entre les applications.

## Choix d'implantation
### SortedDict
Nous avons choisi de réaliser le plus court chemin à l'aide de la structure de données `sortedict` connu
sous le nom de map sur C++. Cela est dû à l'inexistence d'une structure de 
données similiare en python de base.
Ce choix est le résultats d'un test de performance se trouvant sur le fichier `tests/path_test.py`. Ce test
compare les algorithmes de recherche du plus court chemin, utilisant un tas,
une liste chainée et un sortedict.

### OpenGL
Sur OpenGL:
Appuyez sur `n` pour afficher/cacher les normales.
Le mouvement de la caméra se réalise à l'aide des flèches clavier ou les
vim-keybindings (`h`, `j`, `k`, `l`)
ainsi que `z` et `s` pour vous déplacer sur l'axe Z 
Pour les mouvements de caméra nous vous recommandons d'appuyer sur `g` pour afficher
le repère du plan.

Vous pouvez basculer entre deux et trois dimensions en appuyant sur `3`
Vous pouvez changer entre les dimension même lors de l'animation, 
seulement appuyez sur `u`(update) pour mettre à jour le chemin.
Vous pouvez afficher le chemin pendant l'animation en appuyant sur `d`(draw path).

### Tests unitaires
Les tests unitaires se situent dans le dossier `./tests` avec les benchmarks il
néanmoins parfois nécessaire d'attendre un temps important, la génération de
grid etant aleatoire

### PS
Les retours ainsi que les points à améliorer sur le projet serait appreciés.

