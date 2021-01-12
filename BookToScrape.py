import requests
from bs4 import BeautifulSoup
import pandas
import os.path
import urllib
from urllib.request import urlretrieve


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
        list_books[category] = []
        books_url = ['https://books.toscrape.com/catalogue/' + livre.find('a', href=True)['href'][9:] for livre in
                     soup.find_all('div', {'class': 'image_container'})]
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
            next_pages = ['https://books.toscrape.com/catalogue/' + livre.find('a', href=True)['href'][9:] for livre in soup.find_all('div', {'class': 'image_container'})]
            for pages in next_pages:
                books_url.append(pages)
            next = soup.find('li', {'class': 'next'})
        list_books[category] = books_url

    return list_books


def get_info(books_url):
    dictionnary_books = {}
    for category, book in books_url.items():
        dictionnary_books[category] = []
        for books in book:
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
            image_url = 'https://books.toscrape.com/' + soup.find('div', {'class': 'item active'}).find('img')['src'][6:]
            to_add.append(image_url)
            to_add.append(title)
            to_add.append(description)
            to_add.append(upc_book)
            to_add.append(price_ht)
            to_add.append(price_ttc)
            to_add.append(stock)
            to_add.append(stars)
            dictionnary_books[category].append(to_add)

    return dictionnary_books


def dl_images(url):
    if not os.path.exists("./images/"):
        os.mkdir("./images/")
    file = "./images/" + url[len("https://books.toscrape.com/media/cache/fe/72/"):]
    urllib.request.urlretrieve(url, file)


def write_data(data):
    for key, value in data.items():
        for v in value:
            dl_images(v[0])
        df = pandas.DataFrame(value[1:len(value)], columns=['image_url', 'title', 'description', 'upc_book', 'price_ht', 'price_ttc', 'stock', 'stars'])
        df.to_csv(key + '.csv', encoding='utf-8-sig')


urlbooks = 'https://books.toscrape.com/'
response = requests.get(urlbooks)
soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
list_books = {}
result = get_category()
result = get_books(result)
data = get_info(result)
write_data(data)
