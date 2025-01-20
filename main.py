import PySimpleGUIQt as sg

import subprocess
import log

import authentication
import configurator

logger = log.initialize()

configurator.initialize()
cfg = configurator.load("settings.json")
lang = configurator.load("language.json")
text = configurator.load("language.json")[cfg["language"].lower()]


class GUI:
    def __init__(self):
        self.WINDOW_TITLE = "MobilePayAlerts"

        self.event_combiner = {}

        tab_1 = sg.Tab(
            "General",
            [
                [sg.HorizontalSeparator()],
                [sg.Button("Start", key="_BTN_START_", size = (250, 40), visible = True)],
                [sg.HorizontalSeparator()],
                [sg.Button("Stop", key="_BTN_STOP_", size = (250, 40), visible = False)],
                [sg.HorizontalSeparator()],
                [sg.Button("Test", key="_BTN_TEST_", size = (250, 40), visible = True)],
                [sg.HorizontalSeparator()],
            ],
        )

        tab_2 = sg.Tab(
            "Settings",
            [
                [sg.Text("Donation Settings", font = ("def", "def", "bold"))],
                [
                    sg.Text("Default name:", size = (11, 0.6)),
                    sg.InputText(
                        default_text = cfg["default_name"],
                        key = "_INPUT_NAME_",
                        do_not_clear = True,
                        tooltip = "The name that's going to be shown if no name was received from the sender",
                    ),
                ],
                [
                    sg.Text("Default message:", size = (11, 0.6)),
                    sg.InputText(
                        default_text = cfg["default_msg"],
                        key = "_INPUT_MSG_",
                        do_not_clear = True,
                        tooltip = "The text that's going to be shown if no message was received from the sender",
                    ),
                ],
                [
                    sg.Button(
                        "Save Settings",
                        key = "_BTN_SAVE_",
                        tooltip = "Save the current settings",
                    )
                ],
                [sg.HorizontalSeparator()],
                [
                    sg.Text(
                        "Other settings",
                        font = ("def", "def", "bold"),
                    )
                ],
                [
                    sg.Button("Reset", key = "_BTN_RESET_"),
                    sg.Button("Setup", key = "_BTN_SETUP_"),
                ],
            ],
        )

        self.layout = [[sg.TabGroup([[tab_1, tab_2]])]]

    def main(self):
        window = sg.Window(self.WINDOW_TITLE, size = (250, 250)).Layout(self.layout)

        print(window)

        while True:
            event, values = window.Read()
            if event is None or event == "Exit":
                break

            # Main Tab
            if event == "_BTN_START_":
                window.FindElement(event).Update(visible=False)
                # self.receive_alerts = subprocess.Popen(["alerts.exe", "startReceiving"])
                self.receive_alerts = subprocess.Popen(
                    ["python", "alerts.py", "startReceiving"]
                )
                window.FindElement("_BTN_STOP_").Update(visible=True)

            elif event == "_BTN_STOP_":
                window.FindElement(event).Update(visible=False)
                self.receive_alerts.kill()
                window.FindElement("_BTN_START_").Update(visible=True)

            elif event == "_BTN_TEST_":
                window.FindElement(event).Update(visible=False)
                result = subprocess.run(["alerts.exe", "testAlert"])
                window.FindElement(event).Update(visible=True)

            # Settings Tab
            elif event == "_BTN_SAVE_":
                self.save(values)

            elif event == "_BTN_SETUP_":
                Main().setup()

            elif event == "_BTN_RESET_":
                Main().resetConfig()

            elif event in self.event_combiner:
                self.event_combiner[event]()

            print(event, values)

        window.Close()

    def save(self, values):
        cfg["default_name"] = values["_INPUT_NAME_"]
        cfg["default_msg"] = values["_INPUT_MSG_"]
        configurator.save("settings.json", cfg)

class Main:
    def __init__(self):
        logger.info("\n")
        logger.info("Checking for Pushbullet and Streamlabs token")

        if cfg["pb_token"] == "" or cfg["sl_token"] == "":
            sg.PopupOK("Setup", "Setup is required")
            self.setup()

        logger.info("Pushbullet and Streamlabs tokens exist!")

        GUI().main()

    def setup(self):
        logger.info("Starting setup!")
        authentication.runServer()
        logger.info("Setup done!")

    def resetConfig(self):
        logger.info("Resetting config!")
        configurator.save("settings.json", configurator.default("settings.json"))

Main()
