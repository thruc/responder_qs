import requests

data = {'file': ('hello.txt', 'hello, world!', "text/plain")}
r = requests.post('http://127.0.0.1:5042/file', files=data)