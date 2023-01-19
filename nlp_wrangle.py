import pandas as pd
import numpy as np
from env import get_db_url
from bs4 import BeautifulSoup
import requests
from requests import get
import pandas as pd


#------------------- ACQUIRE OR GET DATA -------------------#
def acquire_spam_data():
    '''
    This function reads the zillow data from the Codeup db into a df.
    '''
    # Create SQL query.
    sql_query = """"SELECT * FROM spam"'"""
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_db_url('spam_db'))

    # Save data to csv 
    filepath = Path('spam_db.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index =False)

    # create column message length
    df['message_length'] = df['text'].str.len()
    
    return df


def acquire_codeup_blog():
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = [link['href'] for link in soup.select('.more-link')]

    articles = []

    for url in links:
    
        url_response = get(url, headers=headers)
        soup = BeautifulSoup(url_response.text)
    
        title = soup.find('h1', class_='entry-title').text
        content = soup.find('div', class_='entry-content').text.strip()
    
        article_dict = {
            'title': title,
            'content': content
        }
    
        articles.append(article_dict)
    
    # turns article results into a dataframe
    blog_article_df = pd.DataFrame(articles)
    
    # saves list of articles into csv
    blog_article_df.to_csv('blog_articles.csv', index=False) 

def acquire_news_articles():
    categories = [li.text.lower() for li in soup.select('li')][1:]
    categories[0] = 'national'

    inshorts = []

    for category in categories:
    
        url = 'https://inshorts.com/en/read' + '/' + category
        response = get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        titles = [span.text for span in soup.find_all('span', itemprop='headline')]
        contents = [div.text for div in soup.find_all('div', itemprop='articleBody')]
    
        for i in range(len(titles)):
        
            article = {
                'title': titles[i],
                'content': contents[i],
                'category': category,
            }
        
            inshorts.append(article)
    # creates dataframe of articles 
    inshorts_article_df = pd.DataFrame(inshorts)
    
    # saves articles and contents to csv
    inshorts_article_df.to_csv('news_articles.csv', index=False)

#------------------- GET DATA -------------------#
def get_spam_data():
    '''
    This function reads in zillow data from local copy as a df
    '''
        
    # Reads local copy of csv 
    df = pd.read_csv('spam_db.csv')

    # create column message length
    df['message_length'] = df['text'].str.len()

    return df

def get_codeup_blog_data():
    '''
    This function reads in zillow data from local copy as a df
    '''
        
    # Reads local copy of csv 
    df = pd.read_csv('blog_article.csv')

    return df 

def get_news_articles_data():
    '''
    This function reads in zillow data from local copy as a df
    '''
        
    # Reads local copy of csv 
    df = pd.read_csv('news_articles.csv')

    return df 



