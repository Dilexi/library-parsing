import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import os
from urllib.parse import urljoin, unquote, urlsplit


def check_for_redirect(response):
   if response.history:
      raise requests.exception.HTTPError
   
def download_txt(url, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status() 
    check_for_redirect(response)
    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)

def download_image(image_url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(image_url)
    response.raise_for_status() 
    check_for_redirect(response)
    image_name = urlsplit(image_url).path.split('/')[-1]
    filepath = os.path.join(folder, image_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)

for id in range(1,10):
    try:
        url = f"https://tululu.org/b{id}/"
        response = requests.get(url)
        response.raise_for_status() 
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, 'lxml')
        book_image_url = soup.find('div', class_='bookimage').find('img')['src']
        full_image_url = urljoin('https://tululu.org', book_image_url)
        download_image(full_image_url)
        title = soup.find('h1').text
        book_litle, book_author = title.split(' :: ')
        filename = f'{id}. {book_litle.strip()}'
        url_txt_book = f'https://tululu.org/txt.php?id={id}'
        #download_txt(url_txt_book, filename)
    except:
        print('книга не найдена')