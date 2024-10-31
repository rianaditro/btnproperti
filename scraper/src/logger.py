import logging

def config_logging():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("scraper.log"),
            # logging.StreamHandler() # Console output
        ]
    )