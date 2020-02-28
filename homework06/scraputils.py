import requests
from bs4 import BeautifulSoup
import time


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    tbl_list = parser.table.findAll('table')
    list_of_titles = tbl_list[1].findAll('tr', 'athing')
    list_of_info = tbl_list[1].findAll('td', 'subtext')

    for i in range(len(list_of_titles)):
        score = list_of_info[i].find('span', 'score')
        user = list_of_info[i].find('a', 'hnuser')
        title = list_of_titles[i].find('a', 'storylink')

        if list_of_info[i].text.split()[-1] == 'discuss':
            comments = 0
        elif list_of_info[i].text.split()[-2] == '|':
            comments = 0
        else:
            int(list_of_info[i].text.split()[-2])
            comments = int(list_of_info[i].text.split()[-2])

        news_list.append({'title': title.text,
                          'author': user.text if user else None,
                          'url': title['href'],
                          'comments': comments,
                          'points': int(score.text.split()[0]) if score else 0,

                          })
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    more_page = parser.table.findAll('a', 'morelink')
    return more_page[0]['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        time.sleep(30)
    return news
