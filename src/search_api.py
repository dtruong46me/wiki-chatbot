import requests

class SearchAPI:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.search_engine_id = search_engine_id

    def build_payload(self, query, **params):
        payload = {
            'key': self.api_key,
            'q': query + ' site:vi.wikipedia.org',  # Chỉ tìm kiếm trên Wikipedia tiếng Việt
            'cx': self.search_engine_id
        }
        payload.update(params)
        return payload

    def make_request(self, payload):
        response = requests.get('https://www.googleapis.com/customsearch/v1', params=payload)
        if response.status_code != 200:
            raise Exception(f'Request failed with status code {response.status_code}')
        return response.json()

    def search(self, query):
        payload = self.build_payload(query)
        response = self.make_request(payload)

        # Lấy link đầu tiên từ kết quả trả về
        for item in response.get('items', []):
            if 'vi.wikipedia.org' in item['link']:  # Kiểm tra nếu link là từ Wikipedia tiếng Việt
                return item['formattedUrl']
        
        return None 
    
# GOOGLE_API_KEY = 'AIzaSyA4CuTf5Jy-ZmeVc5ake7-eyShm0a6jL90'
# SEARCH_ENGINE_ID = '330ff11f78b434b31'

# search_api = SearchAPI(GOOGLE_API_KEY, SEARCH_ENGINE_ID)
# query = 'điện thoại'
# result = search_api.search(query)
# print(result)