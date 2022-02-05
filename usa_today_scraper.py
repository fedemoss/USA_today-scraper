# -*- coding: utf-8 -*-
"""
@author: mossney


This is a web scraper for the famous American newspaper 'USA Today'. The aim of this project is to get information about 
certain topics from different perspectives. So I started by analyzing which news are relevant in the USA.


------- ADVICE & IP STUFF

This script is intended to work from google colab by default, since you dont use your IP when using this service.

If you want to run the script locally, be aware that, thanks to the many requests, 
out IP can be blocked by the newspaper site. In this case, we would want some kind of IP protection. 

I tried to protect my IP by generating a random number in each request and using that number to sleep the script....
but this is a poor way of protecting my IP...



-------- USING THE SCRIPT

The main function is:
    
    usa_today_scraper(topic)

-Where the topic is the topic we want to search about (ie topic='global warming'). 
 There are going to be news related with this topic. 


The main function returns a PANDAS dataframe with every article found related with the topic inserted.

"""

#Get all Links
def articles_finder(topic):
  topic.replace(' ','%20')
  url = 'https://www.usatoday.com/search/?q={}&page=1'.format(topic)
  response = requests.get(url)
  soup = BS(response.content, 'html.parser')
  url_base = 'https://www.usatoday.com'

  #pages
  total_pages = int(soup.find(attrs={'class':'gnt_se_pgn_count'}).text.split('of ')[1])

  #iterate
  links = []
  for i in range(total_pages):
    url = 'https://www.usatoday.com/search/?q={}&page={}'.format(topic,i+1)
    response = requests.get(url)
    soup = BS(response.content, 'html.parser')

    articles = soup.find(attrs={'class','gnt_pr'}).find_all('a')
    if i == 0 or i==total_pages-1:
      articles = articles[:-total_pages] #remuevo  links innecesarios 
      for article in articles:
        links.append(url_base + article['href'])
    else:
      articles = articles[:-(total_pages+1)]
      for article in articles:
        links.append(url_base + article['href'])
  return links

#Get content
def get_content(links):
  import numpy as np
  import pandas as pd
  content = []
  title = []
  month = []
  day = []
  year = []
  newspaper = []
  for link in links:
    newspaper.append('USA Today')
    try:
      response = requests.get(link)
      soup = BS(response.content, 'html.parser')

      #text
      try:
        paragraphs = soup.find(attrs={'class':'gnt_ar_b'}).find_all('p')
        article_content = []
        for p in paragraphs:
          article_content.append(p.text)
        article_content = " ".join(article_content)
        content.append(article_content)
      except:
        content.append(np.nan)

      #Title
      try:
        title.append(soup.find(name = 'h1', attrs={'class':'gnt_ar_hl'}).text)
      except:
        title.append(np.nan)

      #Date
      try:
        month.append(str(soup.find(name = 'div', attrs={'class':'gnt_ar_dt'})['aria-label']).split('T ')[1].replace(',','').replace('.','').split(' ')[0])
      except:
        month.append(np.nan)
      try:
        day.append(str(soup.find(name = 'div', attrs={'class':'gnt_ar_dt'})['aria-label']).split('T ')[1].replace(',','').replace('.','').split(' ')[1])
      except:  
        day.append(np.nan)
      try:
        year.append(str(soup.find(name = 'div', attrs={'class':'gnt_ar_dt'})['aria-label']).split('T ')[1].replace(',','').replace('.','').split(' ')[2])
      except:  
        year.append(np.nan)

      time.sleep(np.random.uniform(0.5,1)) #Acting as a normal user
    except:
      content.append(np.nan)
      title.append(np.nan)
      month.append(np.nan)
      day.append(np.nan)
      year.append(np.nan)
      print('Link doesn\'t work')

  general_dict = {'Newspaper': newspaper, 'Title': title, 'Month': month, 'Day':day, 'Year':year, 'Link': links, 'Content': content}
  df = pd.DataFrame(general_dict)
  return df

def usa_today_scraper(topic):
  import requests
  from bs4 import BeautifulSoup as BS
  import time
  links = articles_finder(topic)
  df = get_content(links)
  return df