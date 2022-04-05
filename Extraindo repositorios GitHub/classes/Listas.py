import requests
import json


class ListaDeRepositorios():
    def __init__(self, usuario):
        self.usuario = usuario

    def _requisicao_api(self):
        resposta = requests.get(
            f'https://api.github.com/users/Yas190/repos')
        if resposta.status_code == 200:
            return resposta.json()
        else:
            return {"Status Code": resposta.status_code, "Mensagem": "Erro ao chamar API"}

    def imprime_repositorios(self):
        dados_api = self._requisicao_api()
        if type(dados_api) is not int:
            for i in range(len(dados_api)):
                print(dados_api[i]['name'])
        else:
            print(dados_api)
