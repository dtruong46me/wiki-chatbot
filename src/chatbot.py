
import os, sys

from time import sleep
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import underthesea

import nltk
nltk.download('wordnet')

import warnings
warnings.filterwarnings('ignore')


from dotenv import load_dotenv

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(path)

path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(path)

from scrape_api import ScrapingAPI
from search_api import SearchAPI
from utils import load_vi_stopwords

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

class Chatbot:
    def __init__(self):
        self.end_chat = False
        self.do_not_respond = True
        self.got_topic = False

        self.title = None
        self.text_data = []
        self.sentences = []
        self.para_indices = []
        self.current_sent_idx = None

        self.greeting()

        self.punctuation_dict = str.maketrans({p:None for p in punctuation})
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.stopwords = load_vi_stopwords()

    def greeting(self):
        print("\n---------------------------------------------------------------")
        print("\n+ Bott >> Xin chào, tôi là Wiki Chatbot.")
        sleep(0.5)
        print("        |- Bạn có thể chat với tôi về bất kỳ chủ đề nào trên Wikipedia.")
        sleep(1)
        print("        |- Tôi cố gắng phản hồi lại thông tin. Nếu bạn nhập \'more\', tôi sẽ cung cấp cho bạn nhiều thông tin hơn.")
        sleep(1)
        print("        |- Nếu bạn muốn thoát, hãy gõ \'bye\' hoặc \'quit\' hoặc \'exit\' để kết thúc cuộc trò chuyện.")
        sleep(1.2)
        print("\n+ Bott >> Bây giờ, hãy cho tôi biết chủ đề của bạn. (ví dụ: 'máy tính', 'điện thoại', ...)")
        sleep(0.5)

    def chat(self):
        while not self.end_chat:
            self.receive_input()
            
            if self.got_topic:
                if not self.do_not_respond:
                    self.respond()
                
                self.do_not_respond = False

    def receive_input(self):
        user_input = input('\n+ User >> ')
        if user_input.lower().strip() in ['bye', 'quit', 'exit']:
            self.end_chat = True
            print(f'\n+ Bott >> Kết thúc ...')
            sleep(1)
            print(f'\n+ Bott >> Tạm biệt! Bye!\n')
        
        if user_input.lower().strip() == 'more':
            self.do_not_respond = True

            if self.current_sent_idx is not None:
                response = self.text_data[self.para_indices[self.current_sent_idx]]
            
            else:
                response = "Xin lỗi, bạn hãy nhập câu hỏi của bạn trước nhé!"
            
            print(f'\n+ Bott >> {response}')

        if not self.got_topic:
            search_api = SearchAPI(api_key=GOOGLE_API_KEY, search_engine_id=SEARCH_ENGINE_ID)
            url = search_api.search(query=user_input)

            scrape_api = ScrapingAPI(url=url)
            self.title, self.text_data, self.sentences, self.para_indices = scrape_api.scraping_wiki()
            self.got_topic = True

            print(f"\n+ Bott >> Chủ đề của bạn là \'Wikipedia: {self.title}\'. Bắt đầu trò chuyện nào!")

        else:
            self.sentences.append(user_input)
    
    def respond(self):

        vectorizer = TfidfVectorizer(tokenizer=self.preprocess)
        tfidf = vectorizer.fit_transform(self.sentences)
        scores = cosine_similarity(tfidf[-1], tfidf)

        self.current_sent_idx = scores.argsort()[0][-2]
        scores = scores.flatten()
        scores.sort()

        value = scores[-2]

        if value != 0:
            print(f"\n+ Bott >> {self.sentences[self.current_sent_idx]}")
        
        else:
            print(f"\n+ Bott >> ...")
        
        del self.sentences[-1]
    
    def preprocess(self, text: str):
        text = text.lower().strip().translate(self.punctuation_dict)
        words = underthesea.word_tokenize(text)
        words = [w for w in words if w not in self.stopwords]

        return words

# if __name__ == "__main__":
#     chatbot = Chatbot()
#     chatbot.chat()
    # input = input('\n+ User >> ')
    # print(f'\n+ Bott >> {input}')