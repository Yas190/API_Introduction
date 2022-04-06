import requests

todo = {"title": "Mow lawn"}
response = requests.patch("https://jsonplaceholder.typicode.com/todos/10", json=todo)
print(response.json())
