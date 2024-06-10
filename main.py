import requests

for id in range(1,10):
  url = f"https://tululu.org/txt.php?id={id}"

  response = requests.get(url)
  response.raise_for_status() 

  filename = f'book{id}.txt'
  with open(filename, 'wb') as file:
      file.write(response.content)