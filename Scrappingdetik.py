import requests as req
from bs4 import BeautifulSoup as bs
import csv

hades = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def scrape_detik(hal):
    global hades
    a = 1
    for page in range(1, hal):
        url = f'https://www.detik.com/search/searchnews?query=pemilu+2024&sortby=time&page={page}'
        ge = req.get(url, headers=hades).text
        sop = bs(ge, 'lxml')
        li = sop.find('div', class_='list media_rows list-berita')
        lin = li.find_all('article')
        for x in lin:
            link = x.find('a')['href']
            date = x.find('a').find('span', class_='date').text.replace('WIB', '').replace('detikNews', '').split(',')[1]
            headline = x.find('a').find('h2').text
            ge_ = req.get(link, headers=hades).text
            sop_ = bs(ge_, 'lxml')
            content = sop_.find_all('div', class_='detail__body-text itp_bodycontent')
            for x in content:
                x = x.find_all('p')
                y = [y.text for y in x]
                content_ = ''.join(y).replace('\n', '').replace('ADVERTISEMENT', '').replace('SCROLL TO RESUME CONTENT', '')
                print(f'done[{a}] > {headline[0:10]}')
                a += 1
                with open('politik.csv', 'a', newline='', encoding='utf-8') as file:
                    wr = csv.writer(file, delimiter=',')
                    wr.writerow([headline, date, link, content_])

if __name__ == "__main__":
    try:
        halaman = int(input("Masukkan jumlah halaman yang ingin di-scrape: "))
        scrape_detik(halaman)
        print("Scraping selesai. Data disimpan dalam file politik.csv.")
    except ValueError:
        print("Masukkan angka yang valid untuk jumlah halaman.")
