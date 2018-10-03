import json
import config_handler, data_handler, logger

cfg = config_handler.__init__("settings.ini")
log = logger.__init__()

class handleData():
	def Localsite(self, data):
		if "GET /?code=" and "&state=" in data:
			data = data.split()
			pb_code = data[1]
			pb_code = pb_code.replace("/?code=","")
			pb_code = pb_code.replace("&state=","")
			log.info("Received temporary Pushbullet code!")

			return "pushbullet", pb_code

		elif "GET /?code=" in data:
			data = data.split()
			sl_code = data[1]
			sl_code = sl_code.replace("/?code=","")
			log.info("Received temporary Streamlabs code!")

			return "streamlabs", sl_code

class handleJSON():
	def Localsite(self, data):
		json_data = json.loads(data)
		token = json_data["access_token"]
		return token

	def Payments(self, data):
		json_data = json.loads(data)

		if json_data["push"]["application_name"].lower() == "mobilepay" or json_data["push"]["title"].lower() == "mobilepay":
			log.info("Received donation!")

			log.info("Splitting donation data")
			body = json_data["push"]["body"]
			body = body.split()

			# Amount
			log.info("Getting donation amount")
			amount = body[3]
			amount = amount.replace(",", ".", 1)

			# Name
			log.info("Getting donation name")
			if body[7] == "billede":
				name = body[9]
			else:
				name = body[6]

			name = name.replace(":", "")
			name = name.strip()

			if name == "":
				name = cfg.get("Donation","default_name")

			# Message
			log.info("Getting donation message")
			for i in range(len(body)):
				if ":" in body[i]:
					msg = body[i+1:]
					msg = " ".join(msg)
					break
				else:
					msg = ""

				if msg.strip() == "":
					msg = cfg.get("Donation","default_msg")

			log.info("Donation data: {0} - {1} - \"{2}\"".format(name, str(amount), msg))

			return name, msg, amount

		elif json_data["push"]["title"] == "Test notification" and json_data["push"]["application_name"].lower() == "pushbullet":
			log.info("Received test notification via the Pushbullet API")

		else:
			log.info("Unknown data received: {0}".format(json_data))

		return None, None, None
