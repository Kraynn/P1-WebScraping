__________________________
BOOK TO SCRAPE - Projet #1
--------------------------

Le script etl_bts.py a pour fonction de parcourir l'ensemble des pages du site books.toscrape.com et de créeer un CSV 
pour chacune des catégories de livres disponibles comportant les données de la page produit de chacun des livres des différentes catégories.

Le script img_extract.py a pour fonction d'extraire les images de chacuns des livres du site books.toscrape.com dans un dossier intitulé "Img_extract".


______________
HOW TO INSTALL
--------------

Création de l'environnement virtuel:
------------------------------------
Exectuer les commandes suivantes dans l'invité de commande au sein du répertoire local voulu:
>
>python -m venv etl_env

>etl_env\Scripts\activate.bat

>mkdir Img_Extract

___________________________________________________

Importation des scripts:
---------------------------

Téléchargez et extaire le contenu du repertoire github.com/Kraynn/P1-WebScraping dans le répertoire local. 



Ou cloner le répertoire via github en utilisant la commande:
> git clone https://github.com/Kraynn/P1-WebScraping
> 
Puis copier/coller le contenu dans le repertoire local voulu.
__________________________________________________________

Execution des scripts:
----------------------
Excuter les commandes suivantes pour lancer chacun des scripts:
>
>python etl_bts.py

>python img_extract.py
***************************








