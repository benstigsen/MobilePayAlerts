import json
import logging
from os.path import isfile

logger = logging.getLogger("main")

def initialize():
    if not isfile("settings.json"):
        save("settings.json", default())

def save(cfg_file, settings):
    settings = json.dumps(settings, indent=4)

    logger.info(f"Saving settings to {cfg_file}")
    with open(cfg_file, "w") as f:
        f.write(settings)

def load(cfg_file):
    logger.info(f"Loading {cfg_file}")

    settings = {}
    with open(cfg_file) as f:
        settings = json.load(f)

    return settings

def default():
    return {
        "default_msg":  "",
        "default_name": "Anon",

        "pb_token": "",
        "sl_token": "",

        "redirect_uri":       "http://localhost:1337",
        "redirect_uri_short": "localhost",
        "port":               1337
    }
