import logging

formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# Серверный логгер
server_logger = logging.getLogger('_server_')
server_logger.setLevel(logging.INFO)
server_handler = logging.FileHandler("state-machine-coroutine/server.log", encoding='utf-8')
server_handler.setFormatter(formatter)
server_logger.addHandler(server_handler)