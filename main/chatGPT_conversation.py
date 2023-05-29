import time
import requests
from settings.api_key import API_KEY
from settings.settings import MAIN_URL, get_header, get_gson


class ConversationGPT:
    def __init__(self, conversation):
        self.main_url = MAIN_URL
        self.text = conversation

    def post_text_gpt(self):
        count_backup_response = 20
        while count_backup_response != 0:
            response = requests.post(url=MAIN_URL,
                                     headers=get_header(API_KEY),
                                     json=get_gson(self.text)
                                     )
            if response.status_code != 200:
                print('Sending a repeat request,', response.status_code, response.reason,
                      f'number of attempts: {count_backup_response}', )
                time.sleep(15)
                count_backup_response -= 1
            else:
                try:
                    set_json_data = response.json()
                    get_json_data = set_json_data['choices'][0]['message']['content']
                except KeyError:
                    count_backup_response -= 1
                    print('Json invalid. Sending a repeat request',
                          f' number of attempts: {count_backup_response}')
                    time.sleep(15)
                else:
                    print('Chat gtp says: ' + str(get_json_data) + '\n')
                    count_backup_response -= count_backup_response
                    return str(get_json_data)
            break
