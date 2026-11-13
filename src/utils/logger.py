from logging import getLogger,basicConfig

def log():
    basicConfig(filename='src/utils/atlas_logs.log',)
    logger = getLogger(__name__)
    return logger

