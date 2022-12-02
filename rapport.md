# TDS Projet

1.Contexte du projet

Pour ce projet de traitement de signal, nous avons choisi de faire un lien avec le projet d’intégration. Ce dernier consiste en une application permettant à des jeunes du secondaire d’apprendre le néerlandais. L’apprentissage se fera à travers des jeux et l’accent sera mis sur l’interaction entre les professeurs et les élèves, notamment à travers un suivis détaillé des élèves dans leurs progressions dans les différents niveaux.

Il existe pour l'instant deux modes de jeux dans ce projet : les « FlashCards » et les « DragAndLearn ». Notre objectif est d'en ajouter un troisième en intégrant ce que nous avons appris pendant les cours de traitement de signal. Nous souhaitons donc mettre en place un système qui nous permettrait de vérifier la prononciation des mots en néerlandais.

Par exemple, le site demande à l'élève de prononcer le mot « iedereen » (tout le monde), enregistre le mot prononcé par l'élève et peut lui indiquer si la prononciation était bonne ou mauvaise.

2. Solutions envisagées

Toute la difficulté de ce projet réside dans le fait qu'il faut réussir à identifier une bonne et une mauvaise prononciation. Nous avons murement réfléchis, et deux solutions sont finalement ressorties :

- Utiliser un système de « Speech To Text » (que nous abrégerons par STT)pour vérifier si la personnes prononce bien,
- Analyser le signal reçus et le comparer avec des bons et des mauvais enregistrements.

L'avantage d'avoir deux solutions différentes est que nous pourrons alors comparer les résultats donnés par chacune et améliorer nos prédictions. En effet, leurs résultats pourrons être réunis pour former la décision finale. Il nous faudra donc aussi analyser l'efficacité de chaque solutions pour savoir laquelle est la plus performante et ajuster le poids du résultat de chacune.

Admettons par exemple que le STT ait un taux de détections correctes de 95% mais que la deuxième technique n'ait que 65%, on pourra alors dire que le STT à une plus grande importance dans le décision finale. Par exemple, dans les mêmes suppositions, si le STT nous donne un résultat positif mais que l'autre solutions nous donne un résultat négatif, on pourra quand même envisager une bonne prononciation.

_ **Détaillons maintenant le principe de fonctionnement de chaque solution** \_\_ :_

**A. Speech To Text (STT) :**

Pour cette solution nous utiliserons une librairie qui traduira ce qui est dis par l'élève en texte. Le principe est assez simple : Nous partons d'un mot en néerlandais et d'un enregistrement de l'élève qui essaye de prononcer ce mot correctement. Avec l'enregistrement donné au système, nous pouvons comparer la sortie du STT avec le mot d'origine. Si les résultats concordent, c'est que l'élève à bien prononcé le mot, et si ils ne concordent pas, on suppose que la prononciation n'était pas correcte.

**B. Analyser le signal reçus par rapport à des bons et des mauvais exemples :**

Pour cette solution, nous allons beaucoup plus utiliser les notions vu en classe.

Premièrement, il faudra enregistrer des personnes prononçant correctement le mot et des personnes prononçant mal le mot. On pourra ensuite

3. Réalisation des solutions:

1.

- Découper les signaux pour garder que l'information utile (Aymar)

- Prendre les valeurs absolues des signaux découpés (Aymar)

- Faire la moyenne glissante (moving average) de ce qu'on obtient : (Rachid)

2.

- Effectuer une transformée de fourrier (FFT) sur les signaux : (Rachid)

- On fait une moyenne pour tous les spectrogrammes des mauvais signaux et une moyenne pour tous les spectrogrammes des bons signaux (Brice Patson)

3.

Une fois que l'on a ces deux moyennes,

- prendre la FFT des valeurs absolues d'un nouveau signal que l'on a découpé (comme au point 1)

- comparer cela avec les deux moyennes (la moyenne des mauvais signaux et la moyenne des bons signaux) et dire de quelle moyenne on est le plus proche =\> Grâce à cela on peut catégoriser le signal. (Ikram)

4. Conclusion

Nous avons aussi pu voir que la solution de comparaison de signaux était plus efficace que la solution STT. Nous avons donc pu voir que les deux solutions sont efficaces et que nous pouvons les combiner pour obtenir un résultat plus fiable.

5. Annexes
