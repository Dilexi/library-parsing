import requests


def check_for_redirect(response):
   if response.history:
      raise requests.exception.HTTPError
   


for id in range(1,10):
    try:
        url = f"https://tululu.org/txt.php?id={id}"
        response = requests.get(url)
        response.raise_for_status() 
        check_for_redirect(response)
        filename = f'book{id}.txt'
        with open(filename, 'wb') as file:
            file.write(response.content)
    except:
        print('книга не найдена')