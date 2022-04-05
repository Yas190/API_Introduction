import requests
import json

cotacoes = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BR')
cotacoes_dic = cotacoes.json()
cotacao_dolar = cotacoes_dic['USDBRL'] ['bic']

print(cotacao_dolar)