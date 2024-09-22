import re 
import requests
import pandas as pd
from bs4 import BeautifulSoup
import nltk

class ScrapingAPI:
    def __init__(self, url):
        self.url = url
    
    def scraping_wiki(self):
        try:
            text_data = []
            sentences_data = []
            para_indices = []

            data = requests.get(self.url).content
            soup = BeautifulSoup(data, 'html.parser')

            p_data = soup.findAll('p')
            dd_data = soup.findAll('dd')

            p_list = [p for p in p_data]
            dd_list = [dd for dd in dd_data]

            for tag in p_list + dd_list:
                a = []
                for i in tag.contents:
                    if i.name != 'sup' and i.string != None:
                        stripped = ' '.join(i.string.strip().split())
                        a.append(stripped)
                
                text_data.append(' '.join(a))
            
            for i, para in enumerate(text_data):
                sentences = nltk.sent_tokenize(para)
                sentences_data.extend(sentences)
                index = [i] * len(sentences)
                para_indices.extend(index)
            
            title = soup.find('h1').string

            return title, text_data, sentences_data, para_indices
        
        except Exception as e:
            print(f"\n+  Bott >> Lỗi: {e}. Bạn hãy thử chủ đề khác!")

        return data

# if __name__=='__main__':
#     url = "https://vi.wikipedia.org/wiki/Điện_thoại"

#     api = ScrapingAPI(url=url)
    
#     data = api.scraping_wiki()
#     print(data)