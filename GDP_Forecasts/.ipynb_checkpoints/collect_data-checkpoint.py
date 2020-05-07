# Extract Raw Data

import pandas as pd
from tabula import read_pdf
import requests, bs4, time
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from datetime import date
import pickle

def extract_links(soup):
    links =[]
    for div in soup.find_all(name='a', attrs={'class':'gem-c-document-list__item-title'}):
        links.append(div['href'])
    return links

def extract_links_2(soup):
    links =[]
    for div in soup.find_all(name='h2', attrs={'class':'title'}):
        links.append(div.a['href'])
    return links

def get_links():
    links=[]
    url="https://www.gov.uk/government/collections/data-forecasts#database-of-forecasts"
    req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage=urlopen(req).read()
    page_soup = soup(webpage, "html.parser")
    a=extract_links(page_soup)
    for element in a:
        links.append(element)
    return links

def get_sub_links(links):
    sub_links=[]
    for i in links[1:]:
        url='https://www.gov.uk' + i
        req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage=urlopen(req).read()
        page_soup = soup(webpage, "html.parser")
        a=extract_links_2(page_soup)
        for element in a:
            sub_links.append(element)
    return sub_links


def make_links_dict(links,sub_links):
    sub_links_names = []
    for i in links[1:]:
        sub_links_names.append('_'.join(i.split('-')[-2:]))
    links_dict = dict(zip(sub_links_names,sub_links))
    return links_dict


if __name__ == "__main__":
    links_dict = make_links_dict(get_links(),get_sub_links(get_links()))
    data_dict=dict()
    for k in links_dict:
        if k in ['july_2017','april_2017','march_2017','august_2016','april_2016','march_2016','february_2016','january_2016','march_2013']: 
            first = 6
            second = 9
        else:
            first = 5
            second = 8
            
        data_dict[k] = read_pdf(links_dict[k],pages=[first,second])


    with open('C:/Users/lundr/economics/GDP_Forecasts/raw_data/all_data.pkl','wb') as f:
        pickle.dump(data_dict,f)