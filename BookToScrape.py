import requests
from bs4 import BeautifulSoup
import shutil

urlbooks = 'https://books.toscrape.com/'
response = requests.get(urlbooks)
soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
dictionnary_books = {}


def get_category():
    response = requests.get(urlbooks)
    soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
    urlss = soup.find('ul', {'class': 'nav nav-list'})
    category_links = [f"{urlbooks}{links.find('a', href=True)['href']}" for links in urlss.find_all('li')[1:]]
    category_name = [elem.text.replace(' ', '').split()[0] for elem in urlss.find_all('a')[1:]]
    dico_matching = {}
    for i in range(len(category_links)):
        dico_matching[category_links[i]] = category_name[i]

    return dico_matching


def get_books(dico_matching):
    for url, category in dico_matching.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
        dictionnary_books[category] = []
        books_url = ['https://books.toscrape.com/catalogue/' + livre.find('a', href=True)['href'][9:] for livre in
                     soup.find_all('div', {'class': 'image_container'})]
        # return books_url
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
            books_url = ['https://books.toscrape.com/catalogue/' + livre.find('a', href=True)['href'][9:] for livre in
                         soup.find_all('div', {'class': 'image_container'})]
            next = soup.find('li', {'class': 'next'})
            return books_url


def get_info(books_url):
    for books in books_url:
        to_add = []
        response = requests.get(books)
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
        title = soup.find('h1').text
        description = soup.find('meta', {'name': 'description'})['content']
        information = soup.find_all('td')
        upc_book = information[0].text
        price_ht = information[2].text
        price_ttc = information[3].text
        stock = information[5].text
        stars = soup.find_all('p')[2]['class'][1]
        to_add.append(title)
        to_add.append(description)
        to_add.append(upc_book)
        to_add.append(price_ht)
        to_add.append(price_ttc)
        to_add.append(stock)
        to_add.append(stars)
        dictionnary_books[category].append(to_add)
        print(title)


result = get_category()
get_books(result)
result2 = get_books(result)
get_info(result2)

#     image_url = 'https://books.toscrape.com/' + soup.find('div', {'class': 'item active'}).find('img')['src'][6:]
#     to_add.append(image_url)
#     image_books = image_url.split('/')[-1]
#     r = requests.get(image_url, stream=True)
#     if r.status_code == 200:
#         r.raw.decode_content = True
#         with open("./image_books/" + image_books, 'wb') as f:
#             shutil.copyfileobj(r.raw, f)

#     print('Image sccessfully downloaded:', image_books)
# else:
#     print('Image could not be retreived')



