import requests

response = requests.delete("https://jsonplaceholder.typicode.com/todos/10")
print(response.json())
print(response.status_code)