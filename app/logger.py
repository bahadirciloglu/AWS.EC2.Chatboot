import logging

logger = logging.getLogger("kartal_ai")
logger.setLevel(logging.INFO)

# Konsola log yazmak için handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Log formatı
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Handler'ı ekle
if not logger.hasHandlers():
    logger.addHandler(ch)
