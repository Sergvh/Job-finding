import requests
import codecs
import time
from bs4 import BeautifulSoup as BS

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 '
           'Firefox/47.0', 'Accept': 'text/html,application/xhtml+xml,'
           'application/xml;q=0.9,*/*;q=0.8'}

base_url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&' \
           'category=Python'

jobs = []
urls = []

urls.append(base_url)

for url in urls:
    time.sleep(1)
    req = session.get(url, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, "html.parser")
        div = bsObj.find('div', attrs={'id': 'vacancyListId'})

        if div:
            li_list = div.find_all('li', attrs={'class': 'l-vacancy'})
            for li in li_list:
                a = li.find('a', attrs={'class': 'vt'})
                title = a.text
                href = a['href']
                short = "No description"
                company = "No name"
                div = li.find('div', attrs={'class': 'sh-info'})
                short = div.text
                name = li.find('img', attrs={'class': 'f-i'})
                company = name.text
                jobs.append({'href': href,
                             'title': title,
                             'descript': short,
                             'company': company})
template = '<!DOCTYPE html> <html lang="uk"> <head> <meta charset="utf-8"> ' \
           '</head> <body>'
end = '</body> <html>'
content = '<h2> dou.ua </h2>'

for job in jobs:
    content += '<a href="{href}" target="_blank">{title}</a></br><p>' \
               '{descript}' \
               '</p><p>{company}</p></br>'.format(**job)
    content += '<hr/></br></br>'

data = template + content + end

handle = codecs.open('jobs.html', "w", "utf-8")
handle.write(str(data))
handle.close()
