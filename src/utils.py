import os
from typing import List

def load_vi_stopwords() -> List[str]:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vi_stopwords.txt'))
    
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()
    


# a = load_vi_stopwords(path)
# print(a, type(a))