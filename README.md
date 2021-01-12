# BookToScrape
Projet 2 OC
# Présentation 
Le projet permets de récupérer le contenu du site https://books.toscrape.com/index.html via un programme édité en language Python. Cela va effectué un scrapping en naviguant de catégorie en catégorie puis de livre en livre afin d'y ressortir les informations utiles de chaque bouquin. 
product_page_url
    universal_ product_code (upc)
    title
    price_including_tax
    price_excluding_tax
    number_available
    product_description
    category
    review_rating
    image_url
Tout ces éléments seront ensuite répertorié dans des fichiers csv séparé par leurs catégories respectives. Un fichier contenant toutes les images des livres sera égalements créé avec touts les éléments téléchargés. 
# Python 
Afin de faire fonctionner ce programme, il vous faudra installer Python 3.9.0 grace au lien: https://www.python.org/downloads/ et utiliser de préférence Pycharm. 
# Environnement virtuel 

installation de l'environnement virtuel :  
pip install virtualenv

Creer un environnement virtuel:
virtualenv -p python3 env

Activer l'environnement virtuel:
source env/bin/activate

Télécharger les packages neccessaires : 
pip install -r requirements.txt

# Lancement du projet 
 Python BookToScrape.py ou Python3 Booktoscrape.py 
