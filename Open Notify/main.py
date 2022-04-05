import requests
import json

try:
    response = requests.get(f'https://api.open-notify.org/astros.json')
    print(response.status_code)
except:
    print("Problema ao se conectar com a API")
