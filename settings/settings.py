import os

MAIN_URL = 'https://api.openai.com/v1/chat/completions'
OUT_BOX_TEXT = 'Приветствую! Я являюсь искусственным интеллектом, созданным OpenAI. Я обладаю способностью ' \
               'обрабатывать естественный язык и отвечать на вопросы, используя машинное обучение и глубокие ' \
               'нейронные сети. Моя цель - помочь людям в решении различных задач и облегчить их жизнь. ' \
               'Я готов ответить на любые вопросы и помочь вам в любых ваших проектах.'


def get_gson(text):
    json_data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{text}"}],
        "temperature": 0.7
    }
    return json_data


def get_header(api_key):
    header_data = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    return header_data


WIDTH = 600
HEIGHT = 750
X = 700
Y = 150

ICON_PATH = os.path.join(os.path.dirname(__file__), '..', 'icon', 'GPT.ico')