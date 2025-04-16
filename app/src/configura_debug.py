from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG
from logging import critical, error, warning, info, debug
from logging import basicConfig

basicConfig(
	level=INFO,
	filename='app.log',
	filemode='a',
    format='%(levelname)s:%(asctime)s:%(message)s'
)




# import logging
# import sys

# # Configuração do logger
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(levelname)s:%(asctime)s:%(message)s",
#     handlers=[
#         logging.FileHandler("app.log", mode="a"),  # Grava logs em um arquivo
#         logging.StreamHandler(sys.stdout)         # Exibe logs no console
#     ]
# )

# # Forçar flush após cada log
# class FlushingLogger:
#     def __init__(self, logger):
#         self.logger = logger

#     def info(self, message):
#         self.logger.info(message)
#         sys.stdout.flush()  # Força o flush

# # Substituir o logger padrão pelo logger personalizado
# logger = FlushingLogger(logging.getLogger(__name__))