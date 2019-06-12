import sys, json, asyncio
import configurator

log = configurator.LOG.get()
cfg = configurator.CFG().load("settings.json")

class Alerts():
	def __init__(self):
		modules = ("websockets", "requests")

		# Check if required modules are imported
		for module in modules:
			if module not in sys.modules or module not in globals():
				log.info(f"Importing modules: {modules}")
				global websockets, requests
				import websockets, requests
				break

	async def startReceiving(self):
		if "json" not in sys.modules:
			global json
			import json

		log.info("Connecting to Pushbullet WSS stream")
		async with websockets.connect(f"wss://stream.pushbullet.com/websocket/{cfg['pb_token']}") as websocket:
			while True:
				data = await websocket.recv()

				log.info(f"Received data! :{data}:")
				print(f"Received data! :{data}:")

				if "push" and "application_name" in data:
					self.handleData(data)

	def handleData(self, data):
		json_data = json.loads(data)

		name, msg, amount = "", "", ""

		if json_data["push"]["application_name"] == "MobilePay" or json_data["push"]["title"] == "MobilePay":
			log.info("Received donation!")
			log.info(f"Raw data: {json_data}")

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
				name = body[9][1:]
			else:
				name = body[6][1:]

			name = name.strip()

			# Message
			log.info("Getting donation message")
			for i in range(len(body)):
				if ":" in body[i]:
					msg = body[i+1:]
					msg = " ".join(msg)
					break
				else:
					msg = ""

			log.info(f"Donation data: {name} - {amount} - \"{msg}\"")

		elif json_data["push"]["title"].lower() == "test notification" and json_data["push"]["application_name"].lower() == "pushbullet":
			log.info("Received test notification via the Pushbullet API")
			print("Received test notification via the Pushbullet API")

			self.testAlert()

		else:
			log.info(f"Unknown data received: {json_data}")

		if name.strip() == "":
			name = cfg["default_name"]

		if msg.strip() == "":
			msg = cfg["default_msg"]

		if amount.strip() == "":
			amount = None
		else:
			log.info("Triggering donation alert")
			self.triggerAlert(name, msg, amount)

	def triggerAlert(self, name, msg, amount):
		url = "https://streamlabs.com/api/v1.0/donations"

		data = {
			"access_token"	:cfg["sl_token"],
			"name"			:name,
			"identifier"	:"MobilePay",
			"amount"		:amount,
			"currency"		:"DKK",
			"message"		:msg,
		}

		self.request(url, data)

	def testAlert(self):
		print("Test alert!")
		log.info("Sending test alert")
		url = "https://streamlabs.com/api/v1.0/alerts/send_test_alert"

		data = {
			"access_token":cfg['sl_token'],
			"type":"donation",
		}

		self.request(url, data)

	def request(self, url, data):
		response = requests.post(url, data)

		print(f"Alert request returned: \"{response.text}\"")
		log.info(f"Alert request returned: {response}")

if len(sys.argv) < 2:
	print("No function was specified")
	log.error("No function was specified")
else:
	log.info(f"Calling function '{sys.argv[1]}'")	

	# Start function specified in argument
	try:
		asyncio.run(getattr(Alerts(), sys.argv[1])())
	except Exception as err:
		print(err)