import asyncio, websockets, json, logging, os, requests

if os.path.isfile("PbToken.txt"):
	with open("PbToken.txt", "r") as file:
		pb_token = file.read()

if os.path.isfile("SlToken.txt"):
	with open("SlToken.txt", "r") as file:
		sl_token = file.read()

#print("[Started Payments.py]")

logger = logging.getLogger("output")
filelogger = logging.FileHandler("output.log")
formatlogger = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
filelogger.setFormatter(formatlogger)
logger.addHandler(filelogger)
logger.setLevel(logging.INFO)

def handleJSON(data):
	json_data = json.loads(data)

	if "push" in json_data:
		logger.info("[Payments.py] Received push notification!")
		logger.info("[Payments.py] {0}".format(json_data["push"]["application_name"]))
		if json_data["push"]["application_name"].lower() == "mobilepay":

			logger.info("[Payments.py] Received payment!")

			body = json_data["push"]["body"]

			body = body.split()

			# Amount
			amount = body[3]
			amount = amount.replace(",", ".", 1)

			# Name
			if body[7] == "billede":
				name = body[9]
			else:
				name = body[6]

			if ":" in name:
				name = name.replace(":", "")
			else:
				name = "Unknown"

			# Message
			for i in range(len(body)):
				if ":" in body[i]:
					msg = body[i+1:]
					msg = " ".join(msg)
					break
				else:
					msg = ""

			logger.info("[Payments.py] {0} - {1} - \"{2}\"".format(name, amount, msg))

			try:
				name
				msg
				amount = float(amount)
			except Exception as error:
				logger.error("[Payments.py] \"{0}\"".format(error))
				pass
			else:
				triggerAlert(name, msg, amount)

		else:
			#print("Unknown data: {0}".format(json_data))
			logger.info("[Payments.py] Data received: {0}".format(json_data))

def triggerAlert(name, msg, amount):
	url = "https://streamlabs.com/api/v1.0/donations"

	data = {
		"access_token":sl_token,
		"name":name,
		"identifier":"MobilePay",
		"amount":amount,
		"currency":"DKK",
		"message":msg
	}

	logger.info("[Payments.py] Alert requested")
	response = requests.post(url=url, data=data)
	response = response.text
	logger.info("[Payments.py] Alert request returned \"{0}\"".format(response))

async def notifications():
	logger.info("[Payments.py] Connecting to Pushbullet WSS stream")
	async with websockets.connect("wss://stream.pushbullet.com/websocket/{0}".format(pb_token)) as websocket:
			while True:
				data = await websocket.recv()
				if data:
					handleJSON(data)

logger.info("[Payments.py] Starting Pushbullet loop")
asyncio.get_event_loop().run_until_complete(notifications())
