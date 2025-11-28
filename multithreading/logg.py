# logg.py
import logging
import datetime

def setup_logger(name: str, log_file: str) -> logging.Logger:
    """Настройка логгера"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Серверный логгер
server_logger = setup_logger('server', "multithreading/log/server.log")