from duckduckgo_search import DDGS
import pandas as pd

ddgs = DDGS()

#Creating dictionary of necessary questions which will help to gain the information.


queries =   {
                'search_1':['Identify the industry in which Canoo EV operates','Identify the industry size of Canoo Ev','Identify the Identify the industry growth rate of Canoo EV','Identify the industry trends of Canno EV',
                             'Identify the key players in Canoo EV industry'],

                'search_2' : ['Analyse Canoo EV main competitors','Analyse Canoo EV main competitors market share','Analyse Canoo EV main competitors products or services offered','Analyse Canoo EV main competitors pricing strategy',
                              'Analyse Canoo EV main competitors marketing efforts'],

                'search_3' : ['Identify the key trends in Canoo EV market','Identify the change in consumer behaviour in Canoo EV market','Identify the technological advancement in Canoo EV market',
                              'Identify the shift in competitive advancement in Canoo EV market'],

                'search_4' : ['Gather information on Canoo EV financial performance','Gather information on Canoo EV revenue','Gather information on Canoo EV profit margins','Gather information on Canoo EV ROI',
                              'Gather information on Canoo EV expense structure']
            }

from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import requests
ddgs = DDGS()

# Searching for link over the internet

search_url = {}
for query,questions in queries.items():
  for i in questions:
    search_results = ddgs.text(i,max_results=5)                  #Searching for 5 web links related to the necessary questions.
    if i not in search_url:
        search_url[i] = [href['href']  for href in search_results]

search_url              #printing the URL w.r.t to each question

searches = []
search_urls = []
search_content = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',   #To display me as a authentic user scrapping the data
           "Upgrade-Insecure-Requests": "1","DNT": "1",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5",
           "Accept-Encoding": "gzip, deflate"}

for search,urls in search_url.items():
  for url in urls:
    print('Searching for : ',search,"\n")   #Tracking the url being searched
    website = requests.get(url,headers=headers)
    print('URL: ',url,"\n")
    if website!=403:                        #If the website responded 403 error the data will not be requested to scrap.
      soup = BeautifulSoup(website.text,'lxml')
      searches.append(search)
      search_urls.append(url)
      search_content.append(' '.join([i.text for i in soup.find_all('p')]).replace('\n',' ').replace('\t',' ').replace('\r',' '))
    else:
      continue

DataHouse = pd.DataFrame({'Searched':searches,'Link':search_urls,'Website Content':search_content})    #Storing the data in pandas dataframe after would be converted into CSV file

DataHouse.drop(DataHouse[DataHouse['Website Content']==""].index,axis=0,inplace=True)                 #filtering searches which do not resulted emtpy string and removing them from original dataframe

DataHouse.to_csv('Canoo EV.csv',index=False)
