import requests, os

def sendTestAlert():
	if os.path.isfile("SlToken.txt"):
		try:
			access_token
		except:
			with open('SlToken.txt', 'r') as file:
				access_token = file.read()

			url = "https://streamlabs.com/api/v1.0/alerts/send_test_alert"

			data = {
				"access_token":access_token,
				"type":"donation",
			}

			response = requests.post(url=url, data=data)
			return response.text
