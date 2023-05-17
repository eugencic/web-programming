import json

import requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello bot</h1>'


URL = 'https://api.telegram.org/bot6162398123:AAHj_kQmW57PLhPCfzctfnhfrYabAko3kL4/'

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_updates():
    url = URL + 'getUpdates'
    r = requests.get(url)
    write_json(r.json())
    return r.json()
    
def send_message(chat_id, text='bla-bla-bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

def main():
    # r = requests.get(URL + 'getMe')
    # write_json(r.json())
    # r = get_updates()
    # chat_id = r['result'][-1]['message']['chat']['id']
    # send_message(chat_id)
    pass

if __name__ == '__main__':
    #main()
    app.run()
