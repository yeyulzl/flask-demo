import requests

# 1) GET 示例
r = requests.get('http://127.0.0.1:5000/hello', params={'name': 'Alice'})
print('GET /hello ->', r.json())

# 2) POST 示例
r = requests.post('http://127.0.0.1:5000/add',
                  json={'a': 3, 'b': 4})
print('POST /add  ->', r.json())