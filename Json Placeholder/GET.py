import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos/2")
print(response.json())
print(response.status_code)
print(response.headers)
