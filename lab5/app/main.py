from flask import Flask
from flask import jsonify
from flask import request
import json
import requests


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        
        write_json(r)
        
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        
        if '/start' in message:
            start(chat_id)
            
        elif message.startswith('/latest_news'):
            topic = ' '.join(message.split('/latest_news ')[1:]).strip()
            latest_news(chat_id, topic)
        
        return jsonify(r)
    
    return '<h1>Welcome! This is laboratory work Nr.5 of the Web Programming university course.</h1>'


# url of the Telegram Bot HTTP API with the access token
URL = 'https://api.telegram.org/bot6162398123:AAHj_kQmW57PLhPCfzctfnhfrYabAko3kL4/'

# url of the webhook 
# https://api.telegram.org/bot6162398123:AAHj_kQmW57PLhPCfzctfnhfrYabAko3kL4/setWebhook?url=https://f46e-95-65-58-58.ngrok-free.app/

# url of Newsapi HTTP API with the access token 
NEWSAPI_URL = 'https://newsapi.org/v2/everything?q="cats and dogs"&apiKey=e24a1bc98da2479ebe775452c915989e'


# /start command
def start(chat_id):
    bot_url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': 'Welcome! This is laboratory work Nr.5 of the Web Programming university course.'}
    r = requests.post(bot_url, json=answer)
    return r.json()


def latest_news(chat_id, topic):
    if (is_not_empty(topic)):
        api_endpoint = f'https://newsapi.org/v2/everything?q="{topic}"&apiKey=e24a1bc98da2479ebe775452c915989e'
        
        response = requests.get(api_endpoint)
        
        data = json.loads(response.text)
        
        articles = data['articles']
        article_count = 0
        
        parsed_articles = f'Top latest 5 news on topic "{topic}" \n\n'

        for article in articles:
            parsed_article = (f"🔵 {article['title']}\n\n" \
                            f"{article['description']}\n\n" \
                            f"Read more: {article['url']}\n\n" \
                            f"Source: {article['source']['name']}\n\n\n" )
            parsed_articles += parsed_article
            article_count += 1
                
            if article_count == 5:
                break
        
        bot_url = URL + 'sendMessage'
        answer = {'chat_id': chat_id, 'text': parsed_articles}
        r = requests.post(bot_url, json=answer)
        return r.json()
    else: 
        api_endpoint = 'https://newsdata.io/api/1/news?apikey=pub_22338c927a7a4e5d1eeee81226883382c7726&language=en'
        
        response = requests.get(api_endpoint)
        
        data = json.loads(response.text)
        
        articles = data['results']
        article_count = 0
        
        parsed_articles = f'Top latest 5 news \n\n'

        for article in articles:
            parsed_article = (f"🔵 {article['title']}\n\n" \
                            f"{article['description']}\n\n" \
                            f"Read more: {article['link']}\n\n" \
                            f"Source: {article['creator'][0]}\n\n\n" )
            parsed_articles += parsed_article
            article_count += 1
                
            if article_count == 5:
                break
        
        bot_url = URL + 'sendMessage'
        answer = {'chat_id': chat_id, 'text': parsed_articles}
        r = requests.post(bot_url, json=answer)
        return r.json() 
    

def is_not_empty(string):
    return len(string.strip()) != 0


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        

if __name__ == '__main__':
    app.run()
