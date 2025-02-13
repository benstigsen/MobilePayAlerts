import json
import webbrowser
import requests
import logging
import configurator

from http.server import BaseHTTPRequestHandler, HTTPServer
from re import search as regex

logger = logging.getLogger("main")
cfg = configurator.load("settings.json")

# (Local server / Receive data) #
class LocalServer(BaseHTTPRequestHandler):
    def do_GET(self):
        data = self.requestline

        logger.info(f"Received data: {data}")

        html = "<h3>Make sure you have authorized access to both Pushbullet and Streamlabs!</h3>"

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

        AuthHandler().handle_data(data)

# (Pushbullet / Streamlabs credentials (id, secret)) #
def client(service):
    credentials = {
        "pb": {
            "id": "pushbullet_client_id",
            "secret": "pushbullet_client_secret"
        },
        "sl": {
            "id": "streamlabs_client_id",
            "secret": "streamlabs_client_secret"
        },
    }

    return credentials[service]

# (Starting local server / Stopping local server) #
def run_server():
    logger.info("Starting server")

    logger.info("Opening Pushbullet and Streamlabs in the webbrowser")
    webbrowser.open(
        f"https://www.pushbullet.com/authorize?client_id={client('pb')['id']}&redirect_uri={cfg['redirect_uri']}&response_type=code"
    )
    webbrowser.open(
        f"https://www.streamlabs.com/api/v1.0/authorize?client_id={client('sl')['id']}&redirect_uri={cfg['redirect_uri']}&response_type=code&scope=donations.read+donations.create+alerts.write+alerts.create"
    )

    server = HTTPServer((cfg["redirect_uri_short"], cfg["port"]), LocalServer)
    try:
        logger.info("Starting local HTTP server")
        server.serve_forever()
    except StopServer:
        logger.info("Stopped the local HTTP server")
        return

class StopServer(KeyboardInterrupt):
    pass

# (Handling data / Retrieving tokens) #
class AuthHandler:
    # Handle data
    def handle_data(self, data):
        print(data)

        match = regex(r"=([0-9a-zA-Z\.]+)(&|\s)", data)
        if not match:
            return

        url, service = "", ""

        code = str(match[1]).strip()
        if match[2].strip() == "":
            url = "https://streamlabs.com/api/v1.0/token"
            service = "sl"
        else:
            url = "https://api.pushbullet.com/oauth2/token"
            service = "pb"

        logger.info("Received temporary code!")
        self.retrieve_token(code, url, service)

    # Retrieve tokens
    def retrieve_token(self, code, url, service):
        data = {
            "grant_type": "authorization_code",
            "client_id": client(service)["id"],
            "client_secret": client(service)["secret"],
            "redirect_uri": cfg["redirect_uri"],
            "code": code,
        }

        logger.info("Requesting token")
        token = requests.post(url, data)

        logger.info(f"Request returned: {token}")
        print(f"Token Data: {token.text} - {token}")

        cfg[f"{service}_token"] = json.loads(token.text)["access_token"]

        if cfg["pb_token"] != "" and cfg["sl_token"] != "":
            logger.info("Saving tokens to settings.json")
            configurator.save("settings.json", cfg)

            logger.info("Stopping server")
            raise StopServer()
