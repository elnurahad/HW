import requests
from bs4 import BeautifulSoup


url = input("Введите URL-адрес веб-страницы: ")


try:
    response = requests.get(url)
    response.raise_for_status()  
except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе: {e}")
    exit()


soup = BeautifulSoup(response.text, 'html.parser')


links = soup.find_all('a')


print("Список всех ссылок на странице:")
for link in links:
    href = link.get('href')
    if href:  
        print(href)