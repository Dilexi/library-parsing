import os
import requests
import argparse
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, unquote, urlsplit



def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError
   

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
    with open(unquote(filepath), 'wb') as file:
        file.write(response.content)


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_image_url = soup.find('div', class_='bookimage').find('img')['src']
    full_image_url = urljoin('https://tululu.org', book_image_url)
    title = soup.find('h1').text
    book_title, book_author = title.split(' :: ')
    book_comments = soup.find_all('div', class_='texts')
    comments = [comment.find('span', class_='black').text for comment in book_comments]
    books_genres = soup.find('span', class_='d_book').find_all('a')
    books_genres = [genre.text for genre in books_genres]
    book_parameters = {
        "title": book_title.strip(),
        "author": book_author.strip(),
        "image_url": full_image_url,
        "genre": books_genres,
        "comments": comments
    }
    return book_parameters


def main():
    parser = argparse.ArgumentParser(
        description= "Проект скачивает книги и соответствующие им картинки,\
                     а также собирает информацию о книге"
    )
    parser.add_argument("--start_id", type=int,
                        help="Стартовый id книги для скачивания", default=1)
    parser.add_argument("--end_id", type=int,
                        help="Конечный id книги для скачивания", default=10)
    args = parser.parse_args()
    for number in range(args.start_id, args.end_id):
        try:
            url = f"https://tululu.org/b{number}/"
            response = requests.get(url)
            response.raise_for_status() 
            check_for_redirect(response)
            book_image_url = parse_book_page(response)['image_url']
            download_image(book_image_url)
            book_title = parse_book_page(response)['title']
            filename = f'{number}. {book_title.strip()}'
            url_txt_book = f'https://tululu.org/txt.php?id={number}'
            download_txt(url_txt_book, filename)
        except requests.exceptions.HTTPError:
            print('книга не найдена')
   

if __name__=='__main__':
    main()