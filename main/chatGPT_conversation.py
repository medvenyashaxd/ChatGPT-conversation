import time
import requests
from settings.api_key import API_KEY
from settings.settings import MAIN_URL, get_header, get_gson


class ConversationGPT:
    def __init__(self, conversation):
        self.main_url = MAIN_URL
        self.text = conversation

    def post_text_gpt(self):
        count_backup = 5
        while count_backup != 0:
            response = requests.post(url=MAIN_URL,
                                     headers=get_header(API_KEY),
                                     json=get_gson(self.text)
                                     )
            if response.status_code == 200:
                try:
                    set_json_data = response.json()
                    get_json_data = set_json_data['choices'][0]['message']['content']
                    if not get_json_data == 'None':
                        return get_json_data
                    else:
                        count_backup = count_backup - 1
                        pass
                except (KeyError, TypeError):
                    count_backup = count_backup - 1
                    pass
            time.sleep(15)
