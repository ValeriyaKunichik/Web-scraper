import requests
from bs4 import BeautifulSoup
import pandas as pd

def request_github_trending(url):
    return requests.get(url).text

def extract(page):
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find_all(class_='Box-row')
    
def transform(html_repos):
    top25_array = []
    for row in html_repos:
        title = row.find(class_ = 'h3').get_text().replace('\n', '').replace(' ', '').split('/')
        stargazers = row.find(class_ = 'f6').find('a').get_text().replace('\n', '').replace(' ', '').replace(',', '') 
        top25_array.append({'developer': title[0], 'repository_name': title[1], 'nbr_stars': stargazers})                            
    return top25_array

def _format(repositories_data):   
    df = pd.DataFrame(repositories_data) 
    top25_df = df.rename(columns = {'developer': 'Developer', 'repository_name': 'Repository Name', 'nbr_stars': 'Number of Stars'}, inplace = False)
    top25_csv = top25_df.to_csv(index = False)
    return top25_csv

url ="https://github.com/trending"
page = request_github_trending(url)
html_repos = extract(page)
repositories_data = transform(html_repos)
top25_csv= _format(repositories_data)

print (top25_csv)
