__________________________
BOOK TO SCRAPE - Projet #1
--------------------------

Le script etl_bts.py a pour fonction de parcourir l'ensemble des pages du site books.toscrape.com et de créeer un CSV 
pour chacune des catégories de livres disponibles comportant les données de la page produit de chacun des livres des différentes catégories.

Le script img_extract.py a pour fonction d'extraire les images de chacuns des livres du site books.toscrape.com dans un dossier intitulé "Img_extract".
**************************

______________
HOW TO INSTALL
--------------

Création de l'environnement virtuel:
------------------------------------
A partir du répertoire local voulu, exectuez les commandes suivantes dans l'invité de commande:
>
python -m venv etl_env

etl_env\Scripts\activate.bat

mkdir Img_Extract

------------------------------------

Execution des scripts:
----------------------
Excutez les commandes suivantes pour lancer chacun des scripts:
>
python etl_bts.py

python img_extract.py
***************************








