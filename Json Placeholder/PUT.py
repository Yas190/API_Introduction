import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos/10")
print(response.json())

todo = {"userId": 1, "title": "Wash car", "completed": True}
response = requests.put("https://jsonplaceholder.typicode.com/todos/10", json=todo)
print(response.json())
print(response.status_code)
