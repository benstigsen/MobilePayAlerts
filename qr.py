import PySimpleGUIQt as sg
import qrcode

def generate():
	layout = [
			 [sg.Text("Betalinger lavet med MobilePay box, bliver ikke vist på stream!", font=("def", "def", "bold"), text_color="red")],
			 [sg.Text("Det er foreslået at du genererer QR koden,")],
			 [sg.Text("ved at bruge dit boxID fra MobilePay appen.\n")],
			 [sg.Text("Dette gør at dit telefonnummer ikke er bliver vist til alle")],
			 [sg.Text("og du kan også vælge en standard værdi, som der er på startsiden")],
			 [sg.Text("af MobilePay, når brugeren åbner op for appen.\n")],
			 
			 [sg.Text("Telefonnummer / BoxID:"), sg.InputText(default_text="box10549", key="_NUMBER_")],
			 [sg.Text("Predefineret værdi:"), sg.InputText(default_text="0", key="_AMOUNT_")],

			 [sg.Text("")],
			 [sg.Button("Genererer QR kode")]
			 ]

	window = sg.Window("QR code").Layout(layout)

	while True:
		event, values = window.Read()
		if event is None or event == "Exit":
			break

		number = str(values["_NUMBER_"]).lower()
		amount = str(values["_AMOUNT_"]).strip()

		number = number.strip().replace("box", "").replace(" ", "")

		if len(number) > 5 or amount == "0" or amount == "":
			amount = ""
		else:
			amount = f"&amount={amount}"

		url = f"https://mobilepay.dk/box?phone=box{number}{amount}"

		img = qrcode.make(url)
		img = img.resize((320, 320))
		img.save("QR-code.png")

		break

	window.Close()