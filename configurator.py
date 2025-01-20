import json
import logging
from os.path import isfile

# CONFIGURATION
class CFG():
    def __init__(self):
        self.logger = logging.getLogger("main")

        if not isfile("settings.json"):
            self.reset("settings.json")

        if not isfile("language.json"):
            self.reset("language.json")

    def save(self, cfg_file, settings):
        settings = json.dumps(settings, indent=4)

        self.logger.info(f"Saving settings to {cfg_file}")
        with open(cfg_file, "w") as f:
            f.write(settings)

    def load(self, cfg_file):
        self.logger.info(f"Loading {cfg_file}")

        settings = {}
        with open(cfg_file) as f:
            settings = json.load(f)

        return settings

    def reset(self, cfg_file):
        self.save(cfg_file, self.default(cfg_file))

    def default(self, cfg_file):
        settings = {}
        if cfg_file == "settings.json":
            settings = {
                "language": "danish",

                "default_msg":  "",
                "default_name": "Anon",

                "pb_token": "",
                "sl_token": "",

                "redirect_uri":       "http://localhost:1337",
                "redirect_uri_short": "localhost",
                "port":               1337
            }
        else:
            self.logger.debug("Unknown file")

        return settings
