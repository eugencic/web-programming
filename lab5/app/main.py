from flask import Flask
from flask import jsonify
from flask import request
from dotenv import dotenv_values
import json
import requests
import sqlite3


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
            write_json(r)

            chat_id = r['message']['chat']['id']
            message = r['message']['text']

            if message == '/start':
                start(chat_id)
            elif message.startswith('/latest_news'):
                topic = ' '.join(message.split('/latest_news ')[1:]).strip()
                latest_news(chat_id, topic)  
            elif message.startswith('/save_news'):
                news = ' '.join(message.split('/save_news ')[1:]).strip()
                save_news("news.db", chat_id, news)     
            elif message == '/saved_news':
                saved_news("news.db", chat_id)          
            else:
                command_not_found(chat_id)

        return jsonify(r)

    return '<h1>Welcome! This is laboratory work Nr.5 of the Web Programming university course.</h1>'

def start(chat_id):
    bot_url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': 'Welcome! This is laboratory work Nr.5 of the Web Programming university course.\n\nAvailable commands:\n/start\n/latest_news\n/latest_news <your_topic>\n/save_news <your_URL>\n/saved_news'}
    r = requests.post(bot_url, json=answer)
    return r.json()

def latest_news(chat_id, topic):
    if topic and is_not_empty(topic):
        api_endpoint = f'https://newsapi.org/v2/everything?q="{topic}"&apiKey={newsapi_token}'
        
        response = requests.get(api_endpoint)
        
        data = json.loads(response.text)
        
        articles = data['articles']
        article_count = 0
        
        parsed_articles = f'Top 5 latest news on topic "{topic}" \n\n'

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
        
        parsed_articles = f'Top 5 latest news \n\n'

        for article in articles:
            article_description = get_half_string(article['description'])
            
            parsed_article = (f"🔵 {article['title']}\n\n" \
                            f"{article_description}\n\n" \
                            f"Read more: {article['link']}\n\n" \
                            f"Source: {article['source_id']}\n\n\n" )
            parsed_articles += parsed_article
            article_count += 1
                
            if article_count == 5:
                break
        
        bot_url = URL + 'sendMessage'
        answer = {'chat_id': chat_id, 'text': parsed_articles}
        r = requests.post(bot_url, json=answer)
        return r.json()

def create_user_table(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS saved_news(id TEXT, url TEXT)")

    conn.commit()
    conn.close()

def save_news(database_name, chat_id, url):
    if url and is_not_empty(url):
        create_user_table(database_name)
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM saved_news WHERE id = ?', (chat_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            urls = existing_user[1].split(', ')
            if url not in urls:
                new_urls = existing_user[1] + ', ' + url
                cursor.execute('UPDATE saved_news SET url = ? WHERE id = ?', (new_urls, chat_id))        
        else:
            cursor.execute('INSERT INTO saved_news (id, url) VALUES (?, ?)', (chat_id, url))

        conn.commit()
        conn.close()

        bot_url = URL + 'sendMessage'
        answer = {'chat_id': chat_id, 'text': "News saved to the database"}
        r = requests.post(bot_url, json=answer)
        return r.json()
    else:
        bot_url = URL + 'sendMessage'
        answer = {'chat_id': chat_id, 'text': "Please provide a URL"}
        r = requests.post(bot_url, json=answer)
        return r.json()

def saved_news(database_name, chat_id):
    create_user_table(database_name)
    
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute('SELECT url FROM saved_news WHERE id = ?', (chat_id,))
    urls = cursor.fetchone()
    
    conn.close()

    if urls:
        all_parsed_news = f'Saved URLs: \n\n'
        
        urls = urls[0].split(', ')

        for url in urls:
            parsed_news = f'🔵 {url} \n\n'
            all_parsed_news += parsed_news
            
        bot_url = URL + 'sendMessage'
        answer = {'chat_id': chat_id, 'text': all_parsed_news}
        r = requests.post(bot_url, json=answer)
        return r.json()
    else:
        bot_url = URL + 'sendMessage'
        answer = {'chat_id': chat_id, 'text': 'No saved news'}
        r = requests.post(bot_url, json=answer)
        return r.json()

def command_not_found(chat_id):
    bot_url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': 'Command not found'}
    r = requests.post(bot_url, json=answer)
    return r.json()
    
def is_not_empty(string):
    return len(string.strip()) != 0

def get_half_string(string):
    half_length = len(string) // 2
    half = string[:half_length] + "..."
    return half

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
if __name__ == '__main__':
    app.run()
