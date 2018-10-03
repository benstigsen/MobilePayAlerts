from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, webbrowser, subprocess
import main_handler, config_handler, language_handler, logger

cfg = config_handler.__init__("settings.ini")
log = logger.__init__()

lang = language_handler.getLang(cfg.get("Main", "language"))

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        log.info("Initializing: {}".format(self.__class__.__name__))

        # Window Settings
        self.x, self.y, self.w, self.h = 0, 0, 215, 100
        self.setGeometry(self.x, self.y, self.w, self.h)

        self.window = MainWindow(self)
        self.setCentralWidget(self.window)
        self.setWindowTitle(lang["app_main_title"]) # Window Title

        self.setStyleSheet("QMainWindow {{background:{0}}}".format(cfg.get("GUI","main_bg")))
        self.show()

        log.info("Done initializing: {}".format(self.__class__.__name__))



class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        log.info("Initializing: {}".format(self.__class__.__name__))

        stylesheet = """
        QTabBar::tab:selected {{background:{0};}}
        QTabBar::tab:!selected {{background:{1};color:{2};}}
        """.format(cfg.get("GUI","tab_now"), cfg.get("GUI","tab"), cfg.get("GUI","tab_txt"))

        # Initialize tabs
        tab_1 = GeneralWidget()
        tab_2 = SettingsWidget()
        tab_3 = OtherWidget()

        bg_color = self.palette()
        bg_color.setColor(self.backgroundRole(), QtGui.QColor("{0}".format(cfg.get("GUI","win_bg"))))
        tab_1.setAutoFillBackground(True)
        tab_2.setAutoFillBackground(True)
        tab_3.setAutoFillBackground(True)

        tab_1.setPalette(bg_color)
        tab_2.setPalette(bg_color)
        tab_3.setPalette(bg_color)

        # Add tabs
        tab_holder = QtWidgets.QTabWidget()   # Create tab holder
        tab_holder.addTab(tab_1, lang["tab_1_title"]) # Add "tab1" to tab_holder
        tab_holder.addTab(tab_2, lang["tab_2_title"])
        tab_holder.addTab(tab_3, lang["tab_3_title"])
        tab_holder.setStyleSheet(stylesheet)

        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(tab_holder)

        log.info("Done initializing: {}".format(self.__class__.__name__))



class GeneralWidget(QtWidgets.QWidget): # General
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        log.info("Initializing: {}".format(self.__class__.__name__))

        # Buttons
        self.btn_start = CreateGUI.button(lang["btn_start"], lang["btn_start_tt"], self.on_click)
        self.btn_stop = CreateGUI.button(lang["btn_stop"], lang["btn_stop_tt"], self.on_click, enabled=False)
        self.btn_test = CreateGUI.button(lang["btn_test"], lang["btn_test_tt"], self.on_click)

        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_stop)
        layout.addWidget(self.btn_test)
        layout.addStretch()

        log.info("Done initializing: {}".format(self.__class__.__name__))

    @QtCore.pyqtSlot()
    def on_click(self):
        button = self.sender().text()

        if not button == lang["btn_stop"]:
            if cfg.get("Credentials", "sl_token").strip() == "" or cfg.get("Credentials","pb_token").strip() == "":
                CreateGUI.messagebox(self, lang["msgbox_setup_0_t"], lang["msgbox_setup_0"])
                ready = False
            else:
                ready = True

        if button == lang["btn_start"] and ready == True: # Start Button
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)
            log.info("Starting payments_handler.py")
            #self.payments = subprocess.Popen("payments_handler.py", shell=True)
            self.payments = subprocess.Popen("payments_handler.exe")

        elif button == lang["btn_stop"]: # Stop Button
            self.btn_stop.setEnabled(False)
            self.btn_start.setEnabled(True)
            log.info("Stopping payments_handler.py")
            self.payments.kill()

        elif button == lang["btn_test"] and ready == True: # Test Button
            self.btn_test.setEnabled(False)

            log.info("Send test donation")
            try:
                testClass = main_handler.TestAlert()
                response = testClass.request()
                log.info("Test donation returned: {0}".format(response))
            except Exception as err:
                log.error("Test donation returned: {0}".format(err))

            self.btn_test.setEnabled(True)



class SettingsWidget(QtWidgets.QWidget): # Settings
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        log.info("Initializing: {}".format(self.__class__.__name__))

        # Labels
        label_language = CreateGUI.label(lang["language"], "default")

        # Lines
        line_1 = CreateGUI.line()

        # Buttons
        btn_apply = CreateGUI.button(lang["btn_apply"], lang["btn_apply_tt"], self.on_click)
        btn_reset = CreateGUI.button(lang["btn_reset"], lang["btn_reset_tt"], self.on_click)

        # Combobox / Dropdown
        self.combo_language = CreateGUI.combobox(self, [lang["language_danish"], lang["language_english"]])

        # Layout
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(label_language, 0, 0)
        layout.addWidget(self.combo_language, 0, 1)
        layout.addWidget(line_1, 1, 0, 1, 2) #column>, row^, from row, to row
        layout.addWidget(btn_apply, 2, 0)
        layout.addWidget(btn_reset, 2, 1)

        log.info("Done initializing: {}".format(self.__class__.__name__))

    @QtCore.pyqtSlot()
    def on_click(self):
        button = self.sender().text()
        if button == lang["btn_apply"]:
            self.settings_save()
        elif button == lang["btn_reset"]:
            self.settings_restore()
        elif button == lang["btn_setup"]:
            self.setup()

    def settings_save(self):
        log.info("Saving settings")

        language = self.combo_language.currentText()
        language = language.split("/")[0]               # "danish/dansk" get "danish" only

        cfg.set("Main", "language", language.lower())   # Change config setting

        with open("settings.ini", "w") as cfg_file:     # Save config settings
            cfg.write(cfg_file)

        log.info("Saved settings")

        CreateGUI.messagebox(self, lang["msgbox_apply_t"], lang["msgbox_apply"])

    def settings_restore(self):
        log.info("Restoring settings")
        config_handler.resetSettings("settings.ini")
        log.info("Restored settings successfully")

        CreateGUI.messagebox(self, lang["msgbox_apply_t"], lang["msgbox_apply"])


class OtherWidget(QtWidgets.QWidget): # Other
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        log.info("Initializing: {}".format(self.__class__.__name__))

        # Line
        line_1 = CreateGUI.line()

        # Buttons
        btn_setup = CreateGUI.button(lang["btn_setup"], lang["btn_setup_tt"], self.on_click)

        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(btn_setup)
        layout.addWidget(line_1)
        layout.addStretch()

        log.info("Done initializing: {}".format(self.__class__.__name__))

    @QtCore.pyqtSlot()
    def on_click(self):
        button = self.sender().text()
        if button == lang["btn_setup"]:
            self.setup()

    def setup(self):
        log.info("Starting setup")
        setup_server = subprocess.Popen(["python", "setup_handler.py"] + [
        	"<APPLICATION_SECRET>", # Streamlabs Secret
        	"APPLICATION_SECRET"])	# Pushbullet Secret

        log.info("Starting setup - step 1")
        setup_1 = CreateGUI.messagebox(self, "Setup [1/3]", lang["msgbox_setup_1"]) # Pushbullet
        if setup_1 == QtWidgets.QMessageBox.Ok:
            webbrowser.open("https://www.pushbullet.com/authorize?client_id=<CLIENT_ID>&redirect_uri=http%3A%2F%2Flocalhost%3A1337&response_type=code")

        log.info("Starting setup - step 2")
        setup_2 = CreateGUI.messagebox(self, "Setup [2/3]", lang["msgbox_setup_2"]) # Streamlabs
        if setup_2 == QtWidgets.QMessageBox.Ok:
            webbrowser.open("https://www.streamlabs.com/api/v1.0/authorize?client_id=<CLIENT_ID>&redirect_uri=http://localhost:1337&response_type=code&scope=donations.read+donations.create+alerts.write+alerts.create")

        log.info("Starting setup - step 3")
        setup_3 = CreateGUI.messagebox(self, "Setup [3/3]", lang["msgbox_setup_3"])
        if setup_3 == QtWidgets.QMessageBox.Ok:
            pass

        setup_server.kill()

        setup_4 = CreateGUI.messagebox(self, "Apply", lang["msgbox_apply"])
        if setup_4 == QtWidgets.QMessageBox.Ok:
            pass

class CreateGUI():
    def label(text, stylesheet):
        label = QtWidgets.QLabel(text)
        if stylesheet == "default":
            label.setStyleSheet("color:{0}".format(cfg.get("GUI","txt")))

        return label

    def button(text, tooltip, func, enabled=True):
        btn = QtWidgets.QPushButton(text)

        btn.setStyleSheet("background:{0};color:{1};".format(cfg.get("GUI","btn"),cfg.get("GUI","btn_txt")))
        btn.setToolTip(tooltip)
        btn.clicked.connect(func)
        btn.setEnabled(enabled)
        return btn

    def messagebox(class_, title, text):
        msgbox = QtWidgets.QMessageBox.information(class_, title, text)
        return msgbox

    def combobox(class_, items):
        dropdown = QtWidgets.QComboBox(class_)
        dropdown.setStyleSheet("background:{0};color:{1}".format(cfg.get("GUI","dropdwn"),cfg.get("GUI","dropdwn_txt")))
        for item in items:
            dropdown.addItem(item)

        return dropdown

    def line():
        line_ = QtWidgets.QFrame()
        line_.setFrameShape(QtWidgets.QFrame.HLine)
        line_.setFrameShadow(QtWidgets.QFrame.Sunken)
        line_.setStyleSheet("background: {0}; color: {0}".format(cfg.get("GUI","line")))
        return line_

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
