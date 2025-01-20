import sys
import json
import asyncio
import logging
import configurator
import websockets
import requests

logger = logging.getLogger("main")
cfg = configurator.load("settings.json")

class Alerts():
    async def startReceiving(self):
        logger.info("Connecting to Pushbullet WSS stream")
        async with websockets.connect(f"wss://stream.pushbullet.com/websocket/{cfg['pb_token']}") as websocket:
            while True:
                data = await websocket.recv()

                logger.info(f"Received data! :{data}:")
                print(f"Received data! :{data}:")

                buffer = str(data)
                if "push" in buffer and "application_name" in buffer:
                    self.handleData(buffer)

    def handleData(self, data):
        json_data = json.loads(data)

        name, msg, amount = "", "", ""
        if json_data["push"]["application_name"] == "MobilePay" or json_data["push"]["title"] == "MobilePay":
            logger.info("Received donation!")
            logger.info(f"Raw data: {json_data}")

            logger.info("Splitting donation data")
            body = json_data["push"]["body"]
            body = body.split()

            # Amount
            logger.info("Getting donation amount")
            amount = body[3]
            amount = amount.replace(",", ".", 1)

            # Name
            logger.info("Getting donation name")
            if body[7] == "billede":
                name = body[9][1:]
            else:
                name = body[6][1:]
                name = name.strip()

                # Message
                logger.info("Getting donation message")
                for i in range(len(body)):
                    if ":" in body[i]:
                        msg = body[i+1:]
                        msg = " ".join(msg)
                        break

            logger.info(f"Donation data: {name} - {amount} - \"{msg}\"")
        elif json_data["push"]["title"].lower() == "test notification" and json_data["push"]["application_name"].lower() == "pushbullet":
            logger.info("Received test notification via the Pushbullet API")
            print("Received test notification via the Pushbullet API")
            self.testAlert()
        else:
            logger.info(f"Unknown data received: {json_data}")

        if name.strip() == "":
            name = cfg["default_name"]

        if msg.strip() == "":
            msg = cfg["default_msg"]

        if amount.strip() == "":
            amount = None
            return

        logger.info("Triggering donation alert")
        self.triggerAlert(name, msg, amount)

    def triggerAlert(self, name, msg, amount):
        url = "https://streamlabs.com/api/v1.0/donations"

        data = {
            "access_token": cfg["sl_token"],
            "name":         name,
            "amount":       amount,
            "message":      msg,
            "identifier":   "MobilePay",
            "currency":     "DKK",
        }

        self.request(url, data)

    def testAlert(self):
        print("Test alert!")
        logger.info("Sending test alert")
        url = "https://streamlabs.com/api/v1.0/alerts/send_test_alert"

        data = {
            "access_token": cfg['sl_token'],
            "type": "donation",
        }

        self.request(url, data)

    def request(self, url, data):
        response = requests.post(url, data)

        print(f"Alert request returned: \"{response.text}\"")
        logger.info(f"Alert request returned: {response}")

        if len(sys.argv) < 2:
            print("No function was specified")
            logger.error("No function was specified")
        else:
            logger.info(f"Calling function '{sys.argv[1]}'")

        # Start function specified in argument
        try:
            asyncio.run(getattr(Alerts(), sys.argv[1])())
        except Exception as err:
            print(err)
