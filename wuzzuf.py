import csv
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest

job_title, loca, fall_part_time, req, links, companies = [], [], [], [], [], []

page_num = 0

while True:
    try:
        start_link = f'https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}'
        open_link = requests.get(start_link)
        page = open_link.content
        soup = BeautifulSoup(page, 'lxml')

        page_limit = int(soup.find('strong').text)

        if (page_num > page_limit // 15):
            print('all done')
            break

        job_name = soup.find_all('h2', class_='css-m604qf')
        location = soup.find_all('span', class_='css-5wys0k')
        job_time = soup.find_all('span', class_='css-1ve4b75')
        skills = soup.find_all('div', class_='css-y4udm8')
        company_name = soup.find_all('div', class_='css-d7j1kk')

        for i in range(len(job_name)):
            job_title.append(job_name[i].text)
            links.append(
                f"https://wuzzuf.net{job_name[i].find('a').attrs['href']}")
            loca.append(location[i].text)
            fall_part_time.append(job_time[i].text)
            req.append(skills[i].text)
            companies.append(company_name[i].text)
        page_num += 1
        print('onther page')
    except:
        print('we have a problem')
        break

file_lst = [job_title, companies, loca,
            fall_part_time, req, links]
export = zip_longest(*file_lst)

with open('./wuzzuf.csv', 'w', newline='') as handl:
    write = csv.writer(handl)
    write.writerow(['job_title', 'companies', 'location',
                    'job_time', 'skills', 'links'])
    write.writerows(export)
