import requests
import codecs
import time
import datetime
from bs4 import BeautifulSoup as BS

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 '
           'Firefox/47.0', 'Accept': 'text/html,application/xhtml+xml,'
           'application/xml;q=0.9,*/*;q=0.8'}

base_url = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2?period=' \
           '2&lastdate='

domain = 'https://rabota.ua'
jobs = []
urls = []
yesterday = datetime.date.today()-datetime.timedelta(1)
one_day_ago = yesterday.strftime('%d.%m.%Y')
base_url = base_url + one_day_ago

urls.append(base_url)
req = session.get(base_url, headers=headers)

if req.status_code == 200:
    bsObj = BS(req.content, "html.parser")
    pagination = bsObj.find('dl', attrs={'id': 'ctl00_content_vacancyList_'
                                               'gridList_ctl23_'
                                               'pagerInnerTable'})

    if pagination:
        pages = pagination.find_all('a', attrs={'class': 'f-always-blue'})
        for page in pages:
            urls.append(domain + page['href'])

    #print(urls)

for url in urls:
    time.sleep(1)
    req = session.get(url, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, "html.parser")
        article_list = bsObj.find_all('article', attrs=
        {'class': 'f-vacancylist-vacancyblock'})
        for article in article_list:
            title_all = article.find('h3')
            title = title_all.find('a')
            title = title.text
            href = title_all.a['href']
            short = article.find('p', attrs={'class':
                                             'f-vacancylist-shortdescr'}).text
            company = article.find('p', attrs={'class':
                                               'f-vacancylist-companyname'})
            company = company.a.text
            jobs.append({'href': domain + href,
                         'title': title,
                         'descript': short,
                         'company': company})
template = '<!DOCTYPE html> <html lang="uk"> <head> <meta charset="utf-8"> ' \
           '</head> <body>'
end = '</body> <html>'
content = '<h2> Work.ua </h2>'

for job in jobs:
    content += '<a href="{href}" target="_blank">{title}</a></br><p>{descript}'\
               '</p><p>{company}</p></br>'.format(**job)
    content += '<hr/></br></br>'

data = template + content + end

handle = codecs.open('robota.html', "w", "utf-8")
handle.write(str(data))
handle.close()
