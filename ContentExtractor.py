import requests
from bs4 import BeautifulSoup
import urllib3
from bs4.element import Comment
from fake_useragent import UserAgent
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

url = input("Masukkan URL: ")

# Cache User-Agent untuk digunakan berulang kali
ua = UserAgent()
headers = {"User-Agent": ua.random}

session = requests.Session()  # Menggunakan session requests
session.headers = headers

try:
    response = session.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.find_all(string=True)
        visible_texts = filter(tag_visible, texts)

        print("Konten Teks:")
        for text in visible_texts:
            cleaned_text = text.strip()
            if cleaned_text:
                print(cleaned_text)
                time.sleep(1)  # Delay untuk setiap 10 teks (misalnya)

        print("Gambar:")
        for image in soup.find_all('img'):
            if 'src' in image.attrs:
                print(image['src'])
                time.sleep(1)  # Delay untuk setiap 10 gambar (misalnya)

        print("Link:")
        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                print(link['href'])
                time.sleep(1)  # Delay untuk setiap 10 link (misalnya)
    else:
        print(f"Gagal mengakses URL dengan status: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Terjadi kesalahan saat mengakses URL: {e}")
