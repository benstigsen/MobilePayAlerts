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

**To make this work with your own application, you need to replace \<CLIENT ID\> and <APPLICATION_ID> on line [215](https://github.com/BenTearzz/MobilePayAlerts/blob/a00be77e901fa834fe7ff3da32fc557193335d91/MobilePayAlerts.py#L215), line [222](https://github.com/BenTearzz/MobilePayAlerts/blob/a00be77e901fa834fe7ff3da32fc557193335d91/MobilePayAlerts.py#L222) and line [227](https://github.com/BenTearzz/MobilePayAlerts/blob/a00be77e901fa834fe7ff3da32fc557193335d91/MobilePayAlerts.py#L227) in MobilePayAlerts.py**

----

### Information:
The graphical user interface (GUI) is written in PyQt5.   
You see the progress and follow the development here on GitHub or on the roadmap here: [Trello Roadmap](https://trello.com/b/j8OdYQ3O)   

**MobilePayAlerts.py**  
`from PyQt5 import QtCore, QtGui, QtWidgets` GUI framework.  
`import sys` used to setup GUI.  
`import webbrowser` used in MobilePayAlerts setup for opening Streamlabs and Pushbullet authentication page.  
`import subprocess` used to start "payments_handler.py" as a child process. Also used to start "setup_handler.py" as a child process with given arguments.  

**main_handler.py**  
`import requests` used to trigger Streamlabs test alert.  

**data_handler.py**  
`import json` to handle data from "payments_handler.py" and "setup_handler.py".  

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

**config_handler.py**  
Imported in "MobilePayAlerts.py", "setup_handler.py", "payments_handler.py" and "data_handler.py". Shortcut for setting config file. Used to save, restore and read from "settings.ini".

**language_handler.py**  
Imported in "MobilePayAlerts.py" to set interface language.  

**logger.py**  
Imported in "MobilePayAlerts.py" "main_handler.py", "setup_handler.py", "payments_handler.py" and "data_handler.py". Allows for easy creation and binding to output log file. 
