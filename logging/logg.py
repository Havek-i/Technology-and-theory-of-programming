import logging

formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# Клиентский логгер
client_logger = logging.getLogger('_client_')
client_logger.setLevel(logging.INFO)
client_handler = logging.FileHandler("client.log")
client_handler.setFormatter(formatter)
client_logger.addHandler(client_handler)

# Серверный логгер
server_logger = logging.getLogger('_server_')
server_logger.setLevel(logging.INFO)
server_handler = logging.FileHandler("server.log")
server_handler.setFormatter(formatter)
server_logger.addHandler(server_handler)