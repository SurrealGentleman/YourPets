import requests
from bs4 import BeautifulSoup


def parse_exhibitions():
    url = 'https://expomap.ru/expo/search/?&q=&sType=conf&th=5&tg=227&area=4&fr=&to=&sort_by=date'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    list_events = list()
    for exhibition_element in soup.find_all('li', class_='cl-item'):
        event = {'title': exhibition_element.find('div', class_='cli-title').text.strip(),
                 'img': 'https://expomap.ru' + exhibition_element.find('div', class_='cli-pict').find('img')['src'],
                 'date': ' '.join(exhibition_element.find('div', class_='cli-date').text.strip().replace('\n', '').split()),
                 'desc': exhibition_element.find('div', class_='cli-descr').text.strip(),
                 'location': ', '.join([link.text for link in exhibition_element.find('div', class_='cli-place').find_all('a')]),
                 'link': 'https://expomap.ru' + exhibition_element.find('div', class_='cli-title').find('a')['href']}
        list_events.append(event)
    return list_events
