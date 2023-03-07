import re
import socket
import sys
from urllib.parse import parse_qs, unquote, urlparse

from bs4 import BeautifulSoup


def access(url):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    start_pos = url.find("//") + 2
    end_pos = url.find("/", start_pos)
    if end_pos == -1:
        host = url[start_pos:]
        path = ""
    else:
        host = url[start_pos:end_pos]
        end_pos_query = url.find("?")
        if end_pos_query == -1:
            end_pos_frag = url.find("#")
            if end_pos_frag == -1:
                end_pos_frag = len(url)
            path = url[end_pos:end_pos_frag]
        else:
            path = url[end_pos:end_pos_query]
    
    port = 80
    try:
        s.connect((host, port))
    except socket.timeout:
        print("Connection timed out.")
        s.close()
        exit()
     
    print("Sending request to", host, "at path", path, "\n")

    request = "GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\n\r\n"
    s.sendall(request.encode())  
    
    response = b""
    try:
        while True:
            buffer_size = 3072
            data = s.recv(buffer_size)
            if not data:
                break
            response += data
    except socket.timeout:
        pass

    content = response.decode()
    body_start = content.find('\r\n\r\n') + 4
    body = content[body_start:]

    soup = BeautifulSoup(body, 'html.parser')
    body = soup.get_text()
    body = ' '.join(body.split())

    print('\nContent:')
    print(body)


def search(search_term):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    host = "www.google.com"
    port = 80 
    
    try:
        s.connect((host, port))
    except socket.timeout:
        print("Connection timed out.")
        s.close()
        exit()
    
    encoded_search_term = search_term.replace(" ", "+")
    request = f'GET /search?q={encoded_search_term} HTTP/1.1\r\nHost: www.google.com\r\n\r\n'
    s.sendall(request.encode())  
    
    response = b""
    try:
        while True:
            buffer_size = 3072
            data = s.recv(buffer_size)
            if not data:
                break
            response += data
    except socket.timeout:
        pass

    print("Top 10 results from Google:")
    print()
        
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.find_all(class_="egMi0 kCrYT")
  
    for i, elem in enumerate(links[:10]):
        title = elem.find('h3').get_text()
        url_elem = elem.find('a')
        url = unquote(url_elem['href'])
        url_match = re.search('(?P<url>https?://[^&\s]+)', url)
        url = url_match.group("url")
        url = unquote(url)
        url = re.sub('&sa=.*', '', url)
        url_parts = urlparse(url)
        url_params = parse_qs(url_parts.query)
        
        if 'url' in url_params:
            url = url_params['url'][0]
            
        print(f'{int(i+1)}. {title}')
        print(f'Access the link: {url}')
        print()  


def help():
    help_message = """Available CLI:
    -u <URL>          # make an HTTP request to the specified URL and print the response
    -s <search-term>  # make an HTTP request to search the term using Google and print top 10 results
    -h                # show this help
Usage: python go2web.py [option] [argument]"""
  
    print(help_message) 
            
if __name__ == "__main__":
    arguments = len(sys.argv)

    if arguments == 3 and sys.argv[1] == '-u':
        url = sys.argv[2]
        access(url)

    if arguments == 3 and sys.argv[1] == '-s':
        search_term = sys.argv[2]
        search(search_term)
        
    if arguments == 2 and sys.argv[1] == '-h':
        help()