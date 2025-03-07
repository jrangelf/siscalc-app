import requests
from src.configura_debug import *

def get_api(url):
    """faz a requisição GET à api por meio da url"""
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data  