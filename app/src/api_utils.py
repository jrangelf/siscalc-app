import requests

def get_api(url):
    """Faz uma requisição GET e retorna os dados da API"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
