import requests
import config_handler, data_handler, logger

cfg = config_handler.__init__("settings.ini")
log = logger.__init__()
log.info("\n")

try:
	sl_token = cfg.get("Credentials", "sl_token").strip()
	pb_token = cfg.get("Credentials", "pb_token").strip()

	log.info("Tokens successfully read!")
except:
	log.info("Couldn't retrieve tokens!")

	sl_token = ""
	pb_token = ""

if sl_token == "" or pb_token == "":
	log.info("Creating Credentials section and values")

	cfg["Credentials"] = {"sl_token":"", "pb_token":""}

	log.info("Writing sections and values to settings.ini")
	with open("settings.ini", "w") as cfg_file:
		cfg.write(cfg_file)

class TestAlert():
	def __init__(self):
		self.url = "https://streamlabs.com/api/v1.0/alerts/send_test_alert"

		self.data = {
			"access_token":cfg.get("Credentials", "sl_token"),
			"type":"donation",
		}

	def request(self):
		response = requests.post(self.url, self.data)
		return response.text
