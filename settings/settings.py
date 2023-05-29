MAIN_URL = 'https://api.openai.com/v1/chat/completions'


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
