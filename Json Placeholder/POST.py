import requests

todo = {"userId": 1, "title": "Buy milk", "completed": False}
response = requests.post("https://jsonplaceholder.typicode.com/todos", json=todo)
print(response.json())