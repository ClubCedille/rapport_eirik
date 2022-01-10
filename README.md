# Rapport Eirik

La présente application remplit le rapport de dépenses que les clubs étudiant
de l'ÉTS peuvent soumettre pour obtenir un remboursement. Les données à
inscrire dans les champs du rapport sont fournies dans un fichier en YAML et,
accessoirement, dans un rapport existant. Cette procédure permet de sauvegarder
des informations générales pour les utiliser dans plusieurs rapports produits
sur une longue période. Elle élimine ainsi les erreurs humaines susceptibles de
survenir pendant la copie de données.

Rapport Eirik dépend de la bibliothèque
[PyPDF2](https://github.com/mstamy2/PyPDF2),
dont la documentation est disponible [ici](https://pythonhosted.org/PyPDF2/).

Son nom est tiré de la chanson norvégienne
[*Eirik Jarl*](https://www.youtube.com/watch?v=WQ3C-1C5XuU) faisant référence à
Eirik Håkonsson. Nidaros, le lieu metionné dans le refrain, est l'ancien nom de
Trondheim, qui était autrefois la capitale de la Norvège.

## Installation

Pour installer Rapport Eirik, téléchargez le dossier compressé contenant le
code source ou utilisez `git clone`.

Ensuite, installez les dépendances en lançant la commande suivante dans le
dossier de l'application.

```
pip install -r requirements.txt
```

Le fichier `requirements.txt` est une liste de toutes les dépendances.

## Contenu minimal

Il faut obligatoirement fournir le fichier `LICENSE` avec l'application.

Les quatre modules suivants contiennent le code source de Rapport Eirik.

* `field_setting_parser.py`
* `fill_expense_report.py`
* `path_arg_checks.py`
* `pypdf2_util.py`

Le modèle de rapport `rapport_depenses.pdf` doit être présent dans le même
dossier que ces modules bien qu'on peut spécifier un autre modèle (voir section
suivante).

Tous ces fichiers constituent le strict minimum nécessaire au fonctionnement de
l'application.

## Utilisation

Rapport Eirik doit être lancée en ligne de commande. Le script à exécuter est
`fill_expense_report.py`. Il peut recevoir les cinq arguments suivants.

* `-e`/`--editable`: un drapeau qui rend modifiable le rapport généré
* `-o`/`--output`: le chemin du rapport généré par l'application
* `-p`/`--pdf_data`: (optionnel) le chemin d'un rapport existant, dont la
valeur des champs sera copiée dans le nouveau rapport
* `-t`/`--template`: (optionnel) le chemin du modèle de rapport
* `-y`/`--yml_data`: le chemin du fichier contenant les données en YAML à
inscrire dans le rapport

L'argument `-h` (*help*) affiche la définition de tous les autres.

```
python fill_expense_report.py -h
```

Les chemins `-o`, `-p` et `-t` doivent avoir l'extension `.pdf`; le chemin `-y`
doit avoir l'exentsion `.yml`. Le modèle de rapport par défaut est
`rapport_depenses.pdf`.

L'exmple suivant produit un rapport modifiable à partir de données en YAML
uniquement.

```
python fill_expense_report.py -y field_setting\random_field_values1.yml -o succès.pdf -e
```

Le prochain exemple produit un rapport non modifiable à partir de la valeur des
champs d'un rapport existant et de données en YAML. En cas de différence, ces
dernières écrasent celles extraites du rapport.

```
python fill_expense_report.py -p rapport_depenses_base.pdf -y field_setting/partial_field_setting.yml -o succès.pdf
```

### Fichiers de données

Le dossier `field_setting` contient des exemples de fichier de données en YAML.
Ils prescrivent la structure du fichier spécifié par l'argument `-y`. Pour
omettre une information, on peut effacer ou mettre en commentaire une ligne
entière ou seulement la partie qui suit un deux-points. Il est aussi permis de
supprimer des éléments des listes. Certaines clés n'admettent qu'un ensemble
déterminé de valeurs. Toutes les dates doivent être de format `aaaa-mm-jj`. Des
valeurs booléennes servent à cocher ou non des cases. Par défaut, les cases ne
sont pas cochées. Ne changez jamais le nom des clés. Des indications
additionnelles sont écrites en commentaire dans les fichiers de données
modèles.

## Contenu supplémentaire

Les scripts `pdf_field_values.py` et `write_field_names.py` ne font pas partie
de Rapport Eirik. Ils sont sauvegardés dans ce dépôt parce qu'ils ont aidé au
développement de l'application en révélant des informations sur les champs du
modèle de rapport de dépenses.
