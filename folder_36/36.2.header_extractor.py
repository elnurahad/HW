import requests
from bs4 import BeautifulSoup


url = input("Введите URL-адрес веб-страницы: ")
level = input("Введите уровень заголовка (h1, h2, h3 и т.д.): ")


if level not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
    print("Некорректный уровень заголовка. Пожалуйста, введите h1, h2, h3, h4, h5 или h6.")
    exit()


try:
    response = requests.get(url)
    response.raise_for_status()  
except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе: {e}")
    exit()


soup = BeautifulSoup(response.text, 'html.parser')


headers = soup.find_all(level)


print(f"Заголовки уровня {level} на странице:")
for header in headers:
    print(f"{header.name}: {header.get_text(strip=True)}")