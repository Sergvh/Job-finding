import requests
import codecs
import time
from bs4 import BeautifulSoup as BS

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 '
           'Firefox/47.0', 'Accept': 'text/html,application/xhtml+xml,'
           'application/xml;q=0.9,*/*;q=0.8'}

base_url = 'https://djinni.co/jobs/?lang=uk&location=%D0%9A%D0%B8%D0%B5%D0%B2&' \
           'page=1&primary_keyword=Python'

domain = 'https://djinni.co'
jobs = []
urls = []

urls.append(base_url)
urls.append(base_url+'&page=2')
urls.append(base_url+'&page=3')

for url in urls:
    time.sleep(1)
    req = session.get(url, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, "html.parser")
        li_list = bsObj.find_all('li', attrs={'class': 'list-jobs__item'})
        for li in li_list:
            div = li.find('div', attrs={'class': 'list-jobs__title'})
            title = div.a.text
            href = div.a['href']
            short = "No Description"
            #company = 'No name'
            descr = li.find('div', attrs={'class': 'list-jobs__description'})
            if descr:
                short = descr.p.text
            jobs.append({'href': domain + href,
                         'title': title,
                         'descript': short,
                         'company': "No name"})
template = '<!DOCTYPE html> <html lang="uk"> <head> <meta charset="utf-8"> ' \
           '</head> <body>'
end = '</body> <html>'
content = '<h2> djinni.co </h2>'

for job in jobs:
    content += '<a href="{href}" target="_blank">{title}</a></br><p>{descript}' \
               '</p><p>{company}</p></br>'.format(**job)
    content += '<hr/></br></br>'

data = template + content + end

handle = codecs.open('jobs.html', "w", "utf-8")
handle.write(str(data))
handle.close()
