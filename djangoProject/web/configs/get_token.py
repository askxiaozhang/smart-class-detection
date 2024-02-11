import os
import json

from loguru import logger
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

def get_all_api():
    out = {
        "AGICN_TOKEN": os.getenv("AGICN_TOKEN"),
    }
    logger.info(json.dumps(out, indent=2, ensure_ascii=False))
    return out

if __name__ == "__main__":
    get_all_api()
