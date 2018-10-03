from http.server import BaseHTTPRequestHandler, HTTPServer
import requests, sys
import data_handler, config_handler, logger

cfg = config_handler.__init__("settings.ini")
log = logger.__init__()

port = 1337

credentials = sys.argv[1:]

sl_secret = credentials[0]
pb_secret = credentials[1]

class getHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		data = self.requestline

		html = """
		<h3>Make sure all steps have been completed!</h3>
		<h3>Vær sikker på at alle trinene er blevet opfyldt!</h3>
		<br>
		<p>Developed by <font color="#33CC33">Benjamin <b>"Tearzz"</b> Stigsen</font></p>
		<p>Udviklet af <font color="#33CC33">Benjamin <b>"Tearzz"</b> Stigsen</font></p>
		"""

		self.send_response(200)
		self.send_header('Content-type', 'text/html; charset=utf-8')
		self.end_headers()
		self.wfile.write(html.encode())

		log.info("Received data: {0}".format(data))

		if "GET /?code=" in data:
			provider, code = data_handler.handleData().Localsite(data)

			log.info("Provider: {0} + Code: {1}".format(provider, code))

			# -- Pushbullet -- #
			if provider == "pushbullet":

				log.info("Getting Pushbullet token")

				# Getting the Pushbullet token
				url = "https://api.pushbullet.com/oauth2/token"

				data = {
					"grant_type":"authorization_code",
					"client_id":"<CLIENT_ID>",
					"client_secret":pb_secret,
					"redirect_uri":"http://localhost:1337",
					"code":code
				}

				log.info("Requesting Pushbullet token")
				token = requests.post(url, data)
				log.info("Pushbullet token request returned: {0}".format(token))
				token = data_handler.handleJSON().Localsite(token.text)

				cfg["Credentials"]["pb_token"] = token

			# -- Streamlabs -- #
			elif provider == "streamlabs":

				log.info("Getting Streamlabs token")

				# Getting the Streamlabs token
				url = "https://streamlabs.com/api/v1.0/token"

				# Getting the Streamlabs token
				data = {
				"grant_type":"authorization_code",
				"client_id":"<CLIENT_ID>",
				"client_secret":sl_secret,
				"redirect_uri":"http://localhost:1337",
				"code":code
				}

				log.info("Requesting Streamlabs token")
				token = requests.post(url, data)
				log.info("Streamlabs token request returned: {0}".format(token))
				token = data_handler.handleJSON().Localsite(token.text)

				cfg["Credentials"]["sl_token"] = token

			else:
				return

			log.info("Writing {0} token to settings.ini".format(provider.capitalize()))

			with open("settings.ini", "w") as cfg_file:
				cfg.write(cfg_file)

server = HTTPServer(('localhost', port), getHandler)
server.serve_forever()
