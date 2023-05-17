from flask import Flask
from flask import jsonify
from flask import request
from dotenv import dotenv_values
import json
import requests


app = Flask(__name__)

env_vars = dotenv_values('.env')

bot_token = env_vars.get('BOT_TOKEN')
newsapi_token = env_vars.get('NEWSAPI_TOKEN')
newsdata_token = env_vars.get('NEWSDATA_TOKEN')

URL = f'https://api.telegram.org/bot{bot_token}/'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()

        if 'message' in r and 'text' in r['message']:
            #write_json(r)

            chat_id = r['message']['chat']['id']
            message = r['message']['text']

            if '/start' in message:
                start(chat_id)

            elif message.startswith('/latest_news'):
                topic = ' '.join(message.split('/latest_news ')[1:]).strip()
                latest_news(chat_id, topic)
            else:
                command_not_found(chat_id)

        return jsonify(r)

    return '<h1>Welcome! This is laboratory work Nr.5 of the Web Programming university course.</h1>'

def start(chat_id):
    bot_url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': 'Welcome! This is laboratory work Nr.5 of the Web Programming university course.\n\nAvailable commands:\n/start\n/latest_news\n/latest_news <your_topic>'}
    r = requests.post(bot_url, json=answer)
    return r.json()

def latest_news(chat_id, topic):
    if (is_not_empty(topic)):
        api_endpoint = f'https://newsapi.org/v2/everything?q="{topic}"&apiKey={newsapi_token}'
        
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
        api_endpoint = f'https://newsdata.io/api/1/news?apikey={newsdata_token}&language=en'
        
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

def command_not_found(chat_id):
    bot_url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': 'Command not found'}
    r = requests.post(bot_url, json=answer)
    return r.json()
    
def is_not_empty(string):
    return len(string.strip()) != 0

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
if __name__ == '__main__':
    app.run()
