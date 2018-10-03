# MobilePayAlerts

#### Requirements:
Required modules:  
**Should already be preinstalled:** *sys, os, subprocess, logging, configparser, webbrowser, json*
* PyQt5
* requests
* asyncio
* psutil
* websockets


All of the required modules can be installed like this: `pip install PyQt5 requests asyncio psutil websockets`  
Or you can install one at a time if you prefer that.

### Information:
The graphical user interface (GUI) is written in PyQt5.   
You see the progress and follow the development here on GitHub or on the roadmap here: [Trello Roadmap](https://trello.com/b/j8OdYQ3O)  
 
**main_handler.py**  
`import requests` used to trigger Streamlabs test alert.

**payments_handler.py**  
`from os import getppid` is used to get parent process ID to check if it's parent process still exists (to make sure that payments_handler.py doesn't just run in the background)  
`from psutil import Process` is used to get the parent ID executable name together with `from os import getppid`.  
`import asyncio` used to run payments_handler.py concurrently to receive Pushbullet data without blocking.  
`import requests` used to trigger Streamlabs donation.  
`import websockets` for connecting to the Pushbullet WSS websocket.  

**setup_handler.py**  
`from http.server import BaseHTTPRequestHandler, HTTPServer` to create a local webserver for receiving Pushbullet and Streamlabs credentials.  
`import requests` used to send POST requests to the Pushbullet and Streamlabs API.  
`import sys` used for receiving parsed arguments when called from the Subprocess module in MobilePayAlerts.py.  


To make this work with your own application, you need to replace \<CLIENT ID\> on line [215](https://github.com/BenTearzz/MobilePayAlerts/blob/a00be77e901fa834fe7ff3da32fc557193335d91/MobilePayAlerts.py#L215), line [222](https://github.com/BenTearzz/MobilePayAlerts/blob/a00be77e901fa834fe7ff3da32fc557193335d91/MobilePayAlerts.py#L222) and line [227](https://github.com/BenTearzz/MobilePayAlerts/blob/a00be77e901fa834fe7ff3da32fc557193335d91/MobilePayAlerts.py#L227) in MobilePayAlerts.py
