import json, logging, sys
from os.path import isfile

# CONFIGURATION
class CFG():
	def __init__(self):
		if not isfile("settings.json"):
			self.reset("settings.json")

		if not isfile("language.json"):
			self.reset("language.json")

	def save(self, cfg_file, settings):
		settings = json.dumps(settings, indent=4)

		log.info(f"Saving settings to {cfg_file}")
		f = open(cfg_file, "w")
		f.write(settings)
		f.close()

	def load(self, cfg_file):
		log.info(f"Loading {cfg_file}")

		with open(cfg_file) as f:
			settings = json.load(f)

		return settings

	def reset(self, cfg_file):
		self.save(cfg_file, self.default(cfg_file))

	def default(self, cfg_file):
		if cfg_file == "settings.json":
			settings = {
				"language": "danish",

				"default_msg"	:"",
				"default_name"	:"Anon",

				"pb_token"		:"",
				"sl_token"		:"",

				"redirect_uri"		:"http://localhost:1337",
				"redirect_uri_short":"localhost",
				"port"				:1337
			}

		else:
			log.debug("Unknown file")
			settings = {}

		return settings

# LOGGER
class LOG():
	def get():
		output_log = logging.getLogger("output")

		if not output_log.handlers:
			filelog = logging.FileHandler("output.log")
			formatlog = logging.Formatter("[Line: %(lineno)d | File: %(filename)s | Func: %(funcName)s] [%(asctime)s] [%(levelname)s]: %(message)s")
			filelog.setFormatter(formatlog)
			output_log.addHandler(filelog)
			output_log.setLevel(logging.INFO)

		return output_log


# Create variables for the entire scope
log = LOG.get()