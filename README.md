# pdf-autofiller

La présente application remplit le rapport de dépenses que les clubs étudiant
de l'ÉTS peuvent soumettre pour obtenir un remboursement. Les données à
inscrire dans les champs du rapport sont fournies dans un fichier en YAML.
Cette procédure permet de sauvegarder des informations générales pour les
utiliser dans plusieurs rapports produits sur une longue période. Elle élimine
ainsi les erreurs humaines susceptibles de survenir pendant la copie de
données.

pdf-autofiller dépend de la bibliothèque
[PyPDF2](https://github.com/mstamy2/PyPDF2),
dont la documentation est disponible [ici](https://pythonhosted.org/PyPDF2/).

## Installation

Pour installer pdf-autofiller, téléchargez le dossier compressé contenant le
code source ou utilisez `git clone`.

Ensuite, installez les dépendances de l'application en lançant la commande
suivante dans le dossier de l'application.

```
pip install -r requirements.txt
```

Le fichier `requirements.txt` est une liste de toutes les dépendances.

## Utilisation

pdf-autofiller doit être lancé en ligne de commande. Le script à exécuter est
`fill_expense_report.py`. Il peut recevoir les quatre arguments suivants.

* `-e`/`--editable`: un drapeau qui rend modifiable le rapport généré
* `-o`/`--output`: le chemin du rapport généré par l'application
* `-s`/`--setting`: le chemin du fichier contenant les données à inscrire
* `-t`/`--template`: (optionnel) le chemin du modèle de rapport

Les chemins `-o` et `-t` doivent avoir l'extension `.pdf`; le chemin `-s` doit
avoir l'exentsion `.yml`. Le modèle de rapport par défaut est
`rapport_depenses.pdf`.

Exemple:

```
python fill_expense_report.py -s field_setting\random_field_values1.yml -o succès.pdf -e
```

L'argument `-h` (*help*) affiche la définition de tous les autres.

```
python fill_expense_report.py -h
```

### Fichiers de données

Le dossier `field_setting` contient des exemples de fichier de données en YAML.
Ils prescrivent la structure du fichier spécifié par l'argument `-s`. Pour
omettre une information, on peut effacer une ligne entière ou seulement la
partie qui suit un deux-points. Il est aussi permis de supprimer des éléments
des listes. Certaines clés n'admettent qu'un ensemble déterminé de valeurs.
Toutes les dates doivent être de format `aaaa-mm-jj`. Des valeurs booléennes
servent à cocher ou non des cases. Par défaut, les cases ne sont pas cochées.
Ne changez jamais le nom des clés. Des indications additionnelles sont écrites
en commentaire dans les fichiers de données modèles.

## Contenu supplémentaire

Les scripts `pdf_field_values.py` et `write_field_names.py` ne font pas partie
de pdf-autofiller. Ils sont sauvegardés dans ce dépôt parce qu'ils ont aidé au
développement de l'application en révélant des informations sur les champs du
modèle de rapport de dépenses.
