import pandas as pd 
import unicodedata
import re
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

def basic_clean(text):
    '''this function will produce cleaned string'''
    # make text all lower case 
    text = text.lower()
    #normalize unicode characters 
    text = unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode('utf-8','ignore')
    # remove anything that is not a number, letter, white space or single quote 
    text = re.sub('[^a-z0-9\'\s]', '', text).split
    return text

def tokenize(text):
    '''this function will tokenize string'''
    #tokenize string, return str false will return words in list
    tokenizer = nltk.tokenize.ToktokTokenizer()
    text = tokenizer.tokenize(text,return_str=True)

    return text

def stem(text):
    '''this function will stem the string'''
    # create the stem
    ps = nltk.porter.PorterStemmer()
    # loop through words in string and apply stem
    stems =[ps.stem(word) for word in text.split()]
    # returns stems joined in one paragraph
    text = ' '.join(stems)
    
    return text

def lemmatize(text):
    'this function will lemmatizze the string'
    #create object to hold lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    # loop through words in string and apply lemmatizer
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    #returns lemmas joined 
    text = ' '.join(lemmas)
    return text
    
def remove_stopwords(text, extra_words = [], exclude_words = []):
    '''this function will remove stopwords in string 
    and return string without stop words'''
    # assign our stopwords from nltk into stopword_list
    stopword_list = stopwords.words('english')
    # utilizing set casting, i will remove any excluded stopwords
    stopword_list = set(stopword_list) - set(exclude_words)
    # add in any extra words to my stopwords set using a union
    stopword_list = stopword_list.union(set(extra_words))
    # split our document by spaces
    words = text.split()
    # every word in our document, as long as that word is not in our stopwords
    filtered_words = [word for word in words if word not in stopword_list]
    # glue it back together with spaces, as it was so it shall be
    string_without_stopwords = ' '.join(filtered_words)
    # return the document back
    return string_without_stopwords

def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords,
                                  extra_words=extra_words,
                                  exclude_words=exclude_words)
    
    df['stemmed'] = df['clean'].apply(stem)
    
    df['lemmatized'] = df['clean'].apply(lemmatize)
    
    return df[['title', column,'clean', 'stemmed', 'lemmatized']]


def prep_spam_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords,
                                  extra_words=extra_words,
                                  exclude_words=exclude_words)

    df['stemmed'] = df['clean'].apply(stem)
    
    df['lemmatized'] = df['clean'].apply(lemmatize)
    
    return df[['label', column,'clean', 'stemmed', 'lemmatized']]

