import requests
from bs4 import BeautifulSoup
import pandas as pd

# this function will get the product url and price
def getData(response):
  # if response is None it means product is 'NA'
  if len(response) <= 0 :
    productURLs.append("NA for France")
    prices.append("NA for France")

  else:
    # get the topmost search result returned by SERPstack
    result = ((response)[0])
    # get url of topmost search result
    url = (result['url'])
    # store product url in list 'productURLs'
    productURLs.append(url)

    # requesting the page
    r = requests.get(url, headers = {'User-agent': 'Chrome'})
    # get html content of the page
    htmlContent = r.content
    # parsing html content using  Beautiful soup
    soup = BeautifulSoup(htmlContent, 'html.parser')

    # get product price
    price = soup.find('span', class_="sales").text
    prices.append(price.strip())

# list variables
searchKeys = []
productURLs = []
prices = []

# reads file line by line and stores as list
with open("C:/Users/SPATE/Downloads/task4.csv") as f:
    contents = f.readlines()
f.close()

# get only 'google search code' from file
for content in contents:
    searchKey = (content.split(","))[2]
    searchKeys.append(searchKey)

for i in range(1, len(searchKeys)-50):
    # setting 'qry' and 'params' for API request
    qry = 'site:oneill.com/fr'+ ' "'+str(searchKeys[i])+'"'
    params = {
        'access_key': 'b631e7a3cdccd75ba5ce39a3d01b1fc9',
        'query': qry,
        'country_code': 'FR'
    }
    # requesting SERPstack API
    api_result = requests.get('http://api.serpstack.com/search', params)
    # get SERP data from API request
    api_response = api_result.json()
    # calling 'getData' function and passing it 'organic_results' from api_response
    getData(api_response['organic_results'])

# again repeating actions of above loop for remaining 'searchKeys'
# in this loop I have given a different 'access_key' because from one key only 100 searches are allowed
for i in range(len(searchKeys)-50, len(searchKeys)):
    print(i)
    qry = 'site:oneill.com/fr'+ ' "'+str(searchKeys[i])+'"'
    params = {
        'access_key': '974c5a990636571be33a1be41364f33d',
        'query': qry,
        'country_code': 'FR'
    }
    api_result = requests.get('http://api.serpstack.com/search', params)
    api_response = api_result.json()
    getData(api_response['organic_results'])

# read data from given file
df = pd.read_csv("C:/Users/SPATE/Downloads/task4.csv")
# appending 'Product Page URL' and 'Price(Euros)' to data
df["Product Page URL"] = productURLs
df["Price(Euros)"] = prices
# updating data in original file
df.to_csv("C:/Users/SPATE/Downloads/task4.csv", index=False, encoding='utf-8-sig')

