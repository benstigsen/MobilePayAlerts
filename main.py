import wx, os, logging, subprocess, time, webbrowser
from pathlib import Path
import TestAlert

# --- LOGGER FILE --- #
if os.path.isfile("output.log"):
	with open("output.log", 'w'): # Clear log file
		pass

logger = logging.getLogger("output")
filelogger = logging.FileHandler("output.log")
formatlogger = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

filelogger.setFormatter(formatlogger)
logger.addHandler(filelogger)
logger.setLevel(logging.INFO)

# --- TAB ONE --- #
class TabOne(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.startButton = wx.Button(self, label="Start", pos=(0, 0))
		self.stopButton = wx.Button(self, label="Stop", pos=(0, 30))
		self.testButton = wx.Button(self, label="Test alert", pos=(0, 60))
		self.stopButton.Disable()

		self.Bind(wx.EVT_BUTTON, self.buttonPress, self.startButton)
		self.Bind(wx.EVT_BUTTON, self.buttonPress, self.stopButton)
		self.Bind(wx.EVT_BUTTON, self.buttonPress, self.testButton)

		# Layout
		v_sizer = wx.BoxSizer(wx.VERTICAL)
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)

		v_sizer.Add(self.startButton, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 1)
		v_sizer.Add(self.stopButton, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 1)
		v_sizer.Add(self.testButton, 0, wx.TOP | wx.EXPAND, 1)

		self.SetSizer(v_sizer)

	def buttonPress(self, btn):
		btn.GetEventObject().Disable()
		btn = btn.GetEventObject().GetLabel()
		if btn == "Start":
			logger.info("[TabOne] Starting MPA alerts")
			self.payments = subprocess.Popen("Payments.py")
			self.stopButton.Enable()
			self.testButton.Disable()
		elif btn == "Stop":
			self.payments.kill()
			logger.info("[TabOne] Stopping MPA alerts")
			self.startButton.Enable()
			self.testButton.Enable()
		elif btn == "Test alert":
			logger.info("[TabOne] Test alert requested")
			self.startButton.Disable()
			self.testButton.Disable()
			response = TestAlert.sendTestAlert()
			logger.info("[TabOne] Test alert returned: \"{0}\"".format(response))
			self.startButton.Enable()
			self.testButton.Enable()

# --- TAB TWO --- #
class TabTwo(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.generateButton = wx.Button(self, label="Generate QR code")
		self.resetButton = wx.Button(self, label="Reset")

		self.Bind(wx.EVT_BUTTON, self.buttonPress, self.generateButton)
		self.Bind(wx.EVT_BUTTON, self.buttonPress, self.resetButton)

		# Layout
		v_sizer = wx.BoxSizer(wx.VERTICAL)
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)

		v_sizer.Add(self.generateButton, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 1)
		v_sizer.Add(self.resetButton, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 1)

		self.SetSizer(v_sizer)

	def buttonPress(self, btn):
		btn = btn.GetEventObject().GetLabel()
		if btn == "Reset":
			answer = wx.MessageDialog(None, "Do you wish to perform first time setup on MobilePayAlerts?", "Reset confirmation", wx.YES_NO).ShowModal()
			if answer == wx.ID_YES:
				try:
					logger.info("[Reset] Deleting token files")
					os.remove("SlToken.txt")
					os.remove("PbToken.txt")

					logger.info("[Reset] Restarting script")

					# Restart
					os.startfile(os.path.realpath(__file__))
					raise SystemExit

				except Exception as error:
					logger.error("[Reset] button returned \"{0}\"".format(error))

		elif btn == "Generate QR code":
			number = wx.TextEntryDialog(self, "Phone number:", "Phone number")
			number.SetValue("12345678")

			if number.ShowModal() == wx.ID_OK:
				number = number.GetValue()
				number = number.replace(" ", "")
				number = number.replace("+45","")
				with wx.FileDialog(self, "Save QR code image as:", wildcard="PNG (*.png)|*.png|JPEG (*.jpg)|*.jpg", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
					fileDialog.SetFilename("QRCode")
					if fileDialog.ShowModal() == wx.ID_CANCEL:
						return
					path = fileDialog.GetPath()
				try:
					img = qrcode.make("https://www.mobilepay.dk/erhverv/betalingslink/betalingslink-svar?phone={0}".format(number))
					img.save(path)
				except:
					import qrcode
					img = qrcode.make("https://www.mobilepay.dk/erhverv/betalingslink/betalingslink-svar?phone={0}".format(number))
					img.save(path)
				del number


# --- TAB THREE --- #
class TabThree(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.helpButton = wx.Button(self, label="Help", pos=(0, 0))
		self.contactButton = wx.Button(self, label="Contact", pos=(0, 30))

		self.Bind(wx.EVT_BUTTON, self.buttonPress, self.helpButton)
		self.Bind(wx.EVT_BUTTON, self.buttonPress, self.contactButton)

		# Layout
		v_sizer = wx.BoxSizer(wx.VERTICAL)
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)

		v_sizer.Add(self.helpButton, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 1)
		v_sizer.Add(self.contactButton, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 1)

		self.SetSizer(v_sizer)

	def buttonPress(self, btn):
		btn = btn.GetEventObject().GetLabel()
		if btn == "Help":
			wx.MessageBox("Try any of the following solutions:\n1) Watch this video: VIDEOLINK\n2) Try going to the \"Settings\" tab and click \"Reset\"\n3) If the problem persists get my contact details by clicking \"Contact\"", "Help", wx.OK)

		elif btn == "Contact":
			wx.MessageBox("Contact\nDetails\nHere", "Contact", wx.OK)

# --- MAIN APPLICATION --- #
class application(wx.Frame):
	def __init__(self, *args, **kwargs):
		super(application, self).__init__(*args, **kwargs)

		# Checking if Pushbullet + Streamlabs Access Token file exists
		logger.info("[Main] Checking token files")
		if os.path.isfile("PbToken.txt") and os.path.isfile("SlToken.txt"):
			firstTimeSetup = False
			logger.info("[Main] PbToken.txt found!")
			logger.info("[Main] SlToken.txt found!")
		else:
			firstTimeSetup = True
			logger.info("[Main] PbToken.txt / SlToken.txt not found!")

		if firstTimeSetup == True:
			answer = wx.MessageDialog(None, "Click OK when you're ready to begin setup", "Setup confirmation", wx.OK | wx.CANCEL).ShowModal()

			if answer == wx.ID_CANCEL:
				logger.info("[Main[Setup]] Clicked \"CANCEL\"")
				raise SystemExit

			logger.info("[Main[Setup]] Starting local server (http://localhost:1337)")
			localsite = subprocess.Popen("Localsite.py")
			
			try:
				# Pushbullet
				logger.info("[Main[Setup]] Starting Pushbullet authorization")
				webbrowser.open("https://www.pushbullet.com/authorize?client_id=<CLIENT ID>&redirect_uri=http%3A%2F%2Flocalhost%3A1337&response_type=code")
				wx.MessageBox("Click OK once Pushbullet access has been authorized", "Authorization [1/2]", wx.OK)

				# Streamlabs
				logger.info("[Main[Setup]] Starting Streamlabs authorization")
				webbrowser.open("https://www.streamlabs.com/api/v1.0/authorize?client_id=<CLIENT ID>&redirect_uri=http://localhost:1337&response_type=code&scope=donations.read+donations.create+alerts.write+alerts.create")
				wx.MessageBox("Click OK once Streamlabs access has been authorized", "Authorization [2/2]", wx.OK)
			
			except Exception as error:
				logger.error(error)
				wx.MessageBox("An error occured, please try again. Please make sure to enable authorization access\n(Error: \"{0}\" has been saved to \"output.log\")".format(error), "Setup error", wx.OK)
				localsite.kill()
				raise SystemExit

			# Change to "localsite.pyw"
			logger.info("[Main[Setup]] Stopping local server (http://localhost:1337)")
			localsite.kill()

			if os.path.isfile("PbCode.txt") and os.path.isfile("SlCode.txt"):
				try:
					logger.info("[Main[Setup]] Removing temporary code files")
					os.remove("PbCode.txt")
					os.remove("SlCode.txt")
				except Exception as error:
					logger.error("[Main[Setup]] \"{0}\"".format(error))
			else:
				if os.path.isfile("PbToken.txt") and os.path.isfile("SlToken.txt"):
					pass
				else:
					wx.MessageBox("An error occured, please restart MobilePayAlerts")
					raise SystemExit

		self.SetSize(50, 50, 175, 150)
		self.Bind(wx.EVT_CLOSE, self.OnExit)
		self.Centre() #self.Move((x, y))
		self.GUI()

	def OnExit(self, event):
		self.Destroy()

	def GUI(self):
		panel = wx.Panel(self)
		tabholder = wx.Notebook(panel)

		tab1 = TabOne(tabholder)
		tabholder.AddPage(tab1, "General")

		tab2 = TabTwo(tabholder)
		tabholder.AddPage(tab2, "Settings")

		tab3 = TabThree(tabholder)
		tabholder.AddPage(tab3, "Other")

		sizer = wx.BoxSizer()
		sizer.Add(tabholder, 1, wx.EXPAND)
		panel.SetSizer(sizer)

		self.SetTitle("MobilePayAlerts")
		self.Show(True)

def main():
	app = wx.App()
	application(None)
	app.MainLoop()

main()
