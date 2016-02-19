from nltk import word_tokenize
import os
from urllib import request
from bs4 import BeautifulSoup as BS
from sklearn.feature_extraction.text import TfidfVectorizer as tfidf
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re


# text scrapping from BBC
def BBC_search_page_num(page_num):
    """(str) -> str
    Go to the next search page on BBC"""
    return 'http://www.bbc.co.uk/search/more?page={}&q=zika%20virus'.format(page_num)

def parse_url (url):
    """Extracting a long string from the HTML"""
    try:
        response = request.urlopen(url)
    except:
        print(url)
    raw = response.read().decode('utf8')
    soup = BS(raw,'html.parser')
    return soup

def BBC_get_urls(parsed_html):
    temp_url = parsed_html.find_all('a', class_ = 'rs_touch')
    link_lst = [link['href'] for link in temp_url]
    return link_lst


def BBC_html2text_general(parsed_html, destination = os.getcwd()):
    """Return a text file with the title as the first line and the body
    as one continuous paragraph. If the url does not have the same layout as
    specified below, the text is not taken and return None."""
    temp_title = parsed_html.find_all('h1',class_ = 'story-body__h1')
    temp_body = parsed_html.find_all('div', class_ = 'map-body')
    if temp_body and temp_title is not None:
        title = [text.get_text() for text in temp_title]
        body = [text.get_text() for text in temp_body]
    else:
        return None
    text = re.sub(r'[^a-zA-Z0-9]','', title[0])
    filename = destination + '/'+ 'BBC_' + text + '.txt'
    with open(filename,'w') as file:
        for text in title:
            file.write(text.strip() + '\n')
        for text in body:
            file.write(text.strip())
            
def BBC_html2text_LAC(parsed_html, destination = os.getcwd()):
    """Basically the same as BBC_html2text_general. 
    This function is catered to a specific format in news article with 'Latin
    America & Caribbean' tag. Hence the name 'LAC'."""
    temp_title = parsed_html.find_all('h1',class_ = 'story-body__h1')
    temp_body = parsed_html.find_all('div', class_ = 'story-body__inner')
    refined_body = []
    for text in temp_body:
        refined_body.extend(text.find_all('p'))
    if temp_title is not None and list(temp_title) != []:
        title = [text.get_text().strip() for text in temp_title]
    else:
        return None  
    if refined_body is not None and list(refined_body) != []:
        body = [text.get_text() for text in refined_body]
    else:
        return None
    filename = destination + '/'+ 'BBC_' + title[0] + '.txt'
    with open(filename,'w') as file:
        for text in title:
            file.write(text.strip() + '\n')
        for text in body:
            file.write(text + ' ')
            
def master_extract(destination):
    for i in range(1,26):
        url = BBC_search_page_num(i)
        soup = parse_url(url)
        link_lst = BBC_get_urls(soup)
        for url in link_lst:
            article_soup = parse_url(url)
            BBC_html2text_LAC(article_soup,destination)

# functions for CBC
def CBC_get_urls(parsed_html):
    """Return a list of urls from the search page"""
    temp_url = parsed_html.find_all('p', class_ = 'g')
    refined = []
    for block in temp_url:
        refined.extend(block.find_all('a', recursive = False))
    link_lst = [link['href'] for link in refined]
    return link_lst    

def CBC_html2text_general(parsed_html, destination = os.getcwd()):
    """Return a text file with the title as the first line and the body
    as one continuous paragraph. If the url does not have the same layout as
    specified below, the text is not taken and return None."""
    temp_title = parsed_html.find_all('h1',class_ = 'story-title beta-text')
    temp_subtitle = parsed_html.find_all('h2', class_ = 'story-deck gamma-text')
    temp_body = parsed_html.find_all('div', class_ = 'story-body alpha-text sclt-article')
    refined_body = []
    for text in temp_body:
        refined_body.extend(text.find_all('p'))
    if temp_title is not None and list(temp_title) != []:
        title = [text.get_text().strip() for text in temp_title]
    else:
        return None
    if temp_subtitle is not None and list(temp_subtitle) != []:
        subtitle = [text.get_text().strip() for text in temp_subtitle]
    else:
        return None    
    if refined_body is not None and list(refined_body) != []:
        body = [text.get_text() for text in refined_body]
    else:
        return None

    filename = destination + '/'+ 'CBC_' + title[0] + '.txt'
    with open(filename,'w') as file:
        for text in title:
            file.write(text + '\n')
        for text in subtitle:
            file.write(text + '\n')
        for text in body:
            file.write(text.strip())
            
def CBC_html2text_extra(parsed_html, destination = os.getcwd()):
    """Return a text file with the title as the first line and the body
    as one continuous paragraph. If the url does not have the same layout as
    specified below, the text is not taken and return None."""
    temp_title = parsed_html.find_all('h1',class_ = 'segment-headline')
    temp_body = parsed_html.find_all('div', class_ = 'segment-content clearfix')
    refined_body = []
    for text in temp_body:
        refined_body.extend(text.find_all('p'))
    if temp_title is not None and list(temp_title) != []:
        title = [text.get_text().strip() for text in temp_title]
    else:
        return None  
    if refined_body is not None and list(refined_body) != []:
        body = [text.get_text() for text in refined_body]
    else:
        return None

    filename = destination + '/'+ 'CBC_' + title[0] + '.txt'
    with open(filename,'w') as file:
        for text in title:
            file.write(text + '\n')
        for text in body:
            file.write(text.strip())
    
def CBC_master_extract(destination):
    """Return a list of urls from the search page"""
    for i in range(0,160,10):
        url = 'http://search.cbc.ca/search?q=Zika+virus&site=CBC-News&site=CBC&output=xml_no_dtd&ie=utf8&oe=UTF-8&safe=high&getfields=*&client=cbc-global&proxystylesheet=cbc-global&proxyreload=1&ulang=en&ip=188.74.64.244&access=p&sort=date:D:L:d1&entqr=3&entqrm=0&entsp=a__date_biasing&wc=200&wc_mc=1&ud=1&start={}'.format(i)
        soup = parse_url(url)
        link_lst = CBC_get_urls(soup)
        for link in link_lst:
            article_soup = parse_url(link)
            CBC_html2text_extra(article_soup,destination)        


# running tf-idf on the downloaded text
def text_doc2lst(directory):
    """ Turning all the article.txt into a list of string, where each string
    is an article."""
    article_lst = os.listdir(directory)
    result = []
    for article in article_lst:
        with open(directory + '/' + article,'r') as file:
            result.append(file.read().replace('\n', '. '))
    return result

result = text_doc2lst('BBC Zika') + text_doc2lst('CBC Zika')
vectorizer = tfidf(stop_words = 'english')
X = vectorizer.fit_transform(result)
idf = vectorizer.idf_
# print(dict(zip(vectorizer.get_feature_names(), idf)))
single_string = ''
for string in result:
    single_string = single_string + string
FD_dict = dict(zip(vectorizer.get_feature_names(), idf))
FD_alpha_dict = {}
for key in FD_dict:
    if key.isalpha():
        FD_alpha_dict[key] = FD_dict[key]
FD_alpha_list = list(FD_alpha_dict.items())


