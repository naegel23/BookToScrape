import requests
from bs4 import BeautifulSoup
import shutil

def get_books_info(books, url, category, dictionnaire_books):

    for livre in books:
        to_add = []
        response = requests.get(livre)
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
        titre = soup.find('h1').text
        description = soup.find('meta', {'name': 'description'})['content']
        information = soup.find_all('td')
        upc_livre = information[0].text
        prix_ht = information[2].text
        prix_ttc = information[3].text
        stock = information[5].text
        print(titre)

        # stars = soup.find_all('p')[2]['class'][1]
        # to_add.append(titre)
        # to_add.append(description)
        # to_add.append(upc_livre)
        # to_add.append(prix_ht)
        # to_add.append(prix_ttc)
        # to_add.append(stock)
        # to_add.append(stars)
# dictionnaire_books = le dic qui contiendra les info des livres , to_add represente les value à ajouter
#     j'ajoute les valeur au dictionnaire_books avec .append toutes les valeurs contenue dans to_add
        dictionnaire_books[category].append(to_add)

        image_url = 'https://books.toscrape.com/' + soup.find('div', {'class': 'item active'}).find('img')['src'][6:]
        to_add.append(image_url)
        image_books = image_url.split('/')[-1]
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open("./image_books/" + image_books, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        #     print('Image sccessfully downloaded:', image_books)
        # else:
        #     print('Image could not be retreived')

urlbooks = 'https://books.toscrape.com/'
response = requests.get(urlbooks)
soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")

if response.ok:
    dictionnaire_books = {}
    urlss = soup.find('ul', {'class': 'nav nav-list'})
    category_links = [f"{urlbooks}{links.find('a', href=True)['href']}" for links in urlss.find_all('li')[1:]]
    category_name = [elem.text.replace(' ', '').split()[0] for elem in urlss.find_all('a')[1:]]
# dico_matching permet de faire matcher l'url des categories avec le nom afin que la clé corresponde aux noms des cate
    dico_matching = {}
    for i in range(len(category_links)):
        dico_matching[category_links[i]] = category_name[i]
        # la clé de dico_matching correspond aux urls de category_links qui sera
    # = au valeur de category_name afin d'afficher les noms à la place des urls mais pouvoir scrapper à partir des urls

# .items montre la key, value d'un dictionnaire
    for url, category in dico_matching.items():
    #     dictionnaire_books = dict()
    #     url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    #     category = "patate"
        response = requests.get(url)
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
        dictionnaire_books[category] = []
        # dictionnaire qui contiendra les valeurs to_add
        books = ['https://books.toscrape.com/catalogue/' + livre.find('a', href=True)['href'][9:] for livre in soup.find_all('div', {'class': 'image_container'})]
        # print(len(books))
        print(url)
        get_books_info(books, url, category, dictionnaire_books)

        next = soup.find('li', {'class': 'next'})
        while next:
            if 'index.html' in url:
                url = url.replace('index.html', next.find('a')['href'])
            elif 'page-' in url:
                url = url[:-6].replace('page', next.find('a')['href'])
            if url[-1] == "-":
                url = url[:len(url) - 1]

            response = requests.get(url)
            soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
            books = ['https://books.toscrape.com/catalogue/' + livre.find('a', href=True)['href'][9:] for livre in
                     soup.find_all('div', {'class': 'image_container'})]
            # variable.append(url) ?
            # print(len(books))
            print(url)
            print("======")
            get_books_info(books, url, category, dictionnaire_books)
            next = soup.find('li', {'class': 'next'})


# https://flake8.pycqa.org/en/latest/