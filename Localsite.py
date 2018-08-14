from http.server import BaseHTTPRequestHandler, HTTPServer
import requests, json, os, logging

logger = logging.getLogger("output")
filelogger = logging.FileHandler("output.log")
formatlogger = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

filelogger.setFormatter(formatlogger)
logger.addHandler(filelogger)
logger.setLevel(logging.INFO)

PORT = 1337

class getHandler(BaseHTTPRequestHandler):
	def handleJSON(self, provider, data): # Streamlabs
		json_data = json.loads(data)
		if provider == "streamlabs":
			sl_token = json_data["access_token"]
			return sl_token
		elif provider == "pushbullet": # Pushbullet
			pb_token = json_data["access_token"]
			return pb_token

	def do_GET(self):
		data = self.requestline

		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(b'You may close the tab now')

		logger.info("[Localsite.py] Received data: {0}".format(data))

		if not os.path.isfile("PbToken.txt") or not os.path.isfile("SlToken.txt"):

			# -- Pushbullet -- #
			if "GET /?code=" and "&state=" in data:
				data = data.split()
				pb_code = data[1]
				pb_code = pb_code.replace("/?code=","")
				pb_code = pb_code.replace("&state=","")
				logger.info("[Localsite.py] Received Pushbullet code!")

				logger.info("[Localsite.py] Writing code to Pushbullet file!")
				with open("PbCode.txt", "w") as file:
					file.write(pb_code)
					file.close()

				data = {
				"grant_type":"authorization_code",
				"client_id":"<CLIENT ID>",
				"client_secret":"<CLIENT SECRET>",
				"redirect_uri":"http://localhost:1337", 
				"code":pb_code
				}

				url = "https://api.pushbullet.com/oauth2/token"

				pb_token = requests.post(url=url, data=data)
				pb_token = self.handleJSON("streamlabs", pb_token.text)
				logger.info("[Localsite.py] Received Pushbullet token!")

				logger.info("[Localsite.py] Writing token to Pushbullet file!")
				with open("PbToken.txt", "w") as file:
					file.write(pb_token)
					file.close()

			# -- Streamlabs -- #
			elif "GET /?code=" in data:
				data = data.split()
				sl_code = data[1]
				sl_code = sl_code.replace("/?code=","")
				logger.info("[Localsite.py] Received Streamlabs code!")

				logger.info("[Localsite.py] Writing code to Streamlabs file!")
				with open("SlCode.txt", "w") as file:
					file.write(sl_code)
					file.close()

				data = {
				"grant_type":"authorization_code",
				"client_id":"<CLIENT ID>",
				"client_secret":"<CLIENT SECRET>",
				"redirect_uri":"http://localhost:1337",
				"code":sl_code
				}

				url = "https://streamlabs.com/api/v1.0/token"

				sl_token = requests.post(url=url, data=data)
				sl_token = self.handleJSON("streamlabs", sl_token.text)

				logger.info("[Localsite.py] Writing token to Streamlabs file!")
				with open("SlToken.txt", "w") as file:
					file.write(sl_token)
					file.close()

			if os.path.isfile("PbToken.txt") and os.path.isfile("SlToken.txt"):
				logger.info("[Localsite.py] PbToken.txt exists!")
				logger.info("[Localsite.py] SlToken.txt exists!")
				raise SystemExit 
		else:
			logger.info("[Localsite.py] PbToken.txt exists!")
			logger.info("[Localsite.py] SlToken.txt exists!")
			raise SystemExit

server = HTTPServer(('localhost', PORT), getHandler)
server.serve_forever()
