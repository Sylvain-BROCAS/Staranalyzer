# Staranalyzer
Une petite interface qui permet d'ouvrir une photo du ciel profond et affiche la luminosité le long de l'image dans deux direction. L'objectif est d'aider à discriminer une image d'étoile d'une image de galaxie à partir de son profile de luminosité.


# Utilisation de logiciel
Pour utiliser ce petit script, il faut d'abord installer python (téléchargement [ici](https://www.python.org/downloads/)).
Télécharger ensuite les fichiers du projet.

Il faut alors installer les modules nécessaires pour faire tourner le programme : 
tapez `py -m pip install -r requirements.txt` dans le cmd

Vous pouvez alors lancer le script, une interface graphique s'ouvre.
--img--

Choisissez d'abord une image à analiser. Choisissez ensuite à l'aide des spinbox les zones de traitement.
Lorsque vous appuyez sur "Trace", le logiciel va afficher l'évolution de la luminosité le long de la vertical et de l'horizontale aux coordonnées spécifiées (c et r), et va moyenner la luminosité sur tout la largeur de la bande (paramètres N et M).

Une fois les graphes générés, il est possible de spécifier un nom de fichier et de sauvegarder la figure. Le fichier se trouvera alors dans le dossier "Result".
