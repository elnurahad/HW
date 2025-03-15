import requests
import re
from collections import Counter

def find_common_words(url_list):
    word_count = Counter()

    for url in url_list:
        try:
            response = requests.get(url)
            response.raise_for_status()
            text = response.text
            words = re.findall(r'\b\w+\b', text.lower())
            word_count.update(words)
        except requests.exceptions.RequestException as e:
            print(f"Error processing URL {url}: {e}")

    most_common_words = word_count.most_common()
    
    return most_common_words

url_list = [
    "https://www.itcareerhub.de",
    "https://www.iqvia.com",
]

common_words = find_common_words(url_list)

for word, count in common_words:
    print(f"{word}: {count}")
    