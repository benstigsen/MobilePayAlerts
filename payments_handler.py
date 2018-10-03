from os import getppid
from psutil import Process
import asyncio, requests, websockets
import data_handler, config_handler, logger

cfg = config_handler.__init__("settings.ini")
log = logger.__init__()

sl_token = cfg.get("Credentials", "sl_token")
pb_token = cfg.get("Credentials", "pb_token")

parent_id = getppid()
parent_exe = Process(parent_id).name()
log.info("{0} process id: {1}".format(parent_exe, parent_id))

async def notifications():
	log.info("Connecting to Pushbullet WSS stream")
	async with websockets.connect("wss://stream.pushbullet.com/websocket/{0}".format(pb_token)) as websocket:
		while True:
			data = await websocket.recv()

			if Process(parent_id).name() != parent_exe:
				log.debug("Parent process isn't available, closing self")
				raise SystemExit

			if "push" and "application_name" in data:
				name, msg, amount = data_handler.handleJSON().Payments(data)

				if name != None and msg != None and amount != None:
					log.info("Triggering donation alert")
					triggerAlert(name, msg, amount)

def triggerAlert(name, msg, amount):
	url = "https://streamlabs.com/api/v1.0/donations"

	data = {
		"access_token":sl_token,
		"name":name,
		"identifier":"MobilePay",
		"amount":amount,
		"currency":"DKK",
		"message":msg,
	}

	log.info("Alert request has been sent!")
	response = requests.post(url, data)
	log.info("Alert request returned: \"{0}\"".format(response.text))

asyncio.get_event_loop().run_until_complete(notifications())
