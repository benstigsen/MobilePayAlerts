import tkinter as tk
from tkinter import ttk
import alerts
import asyncio
import configurator
import authentication
import log
import sv_ttk

logger = log.initialize()

configurator.initialize()
cfg = configurator.load("settings.json")

root = tk.Tk()
def callback(name):
    return lambda: button(name)

def widget_by_name(tab, name):
    return root.nametowidget(f"_MAIN_._TAB{tab}_.{name}")

def enable(tab, name):
    widget_by_name(tab, name)["state"] = "normal"

def disable(tab, name):
    widget_by_name(tab, name)["state"] = "disable"

def button(name):
    match name:
        case "_BTN_START_":
            disable(1, name)
            asyncio.run(alerts.start_receiving())
            enable(1, "_BTN_STOP_")
        case "_BTN_STOP_":
            disable(1, name)
            for task in asyncio.all_tasks():
                task.cancel()
            enable(1, "_BTN_START_")
        case "_BTN_TEST_":
            disable(1, name)
            asyncio.run(alerts.test_alert())
            enable(1, name)
        case "_BTN_SAVE_":
            cfg["default_name"] = widget_by_name(2, "_INPUT_NAME_").get()
            cfg["default_msg"] = widget_by_name(2, "_INPUT_MSG_").get()
            configurator.save("settings.json", cfg)
        case "_BTN_SETUP_":
            logger.info("Starting setup!")
            authentication.run_server()
            logger.info("Setup done!")
        case "_BTN_RESET_":
            logger.info("Resetting config!")
            configurator.save("settings.json", configurator.default())
            widget_by_name(2, "_BTN_RESET_").invoke()

def main():
    root.title("MobilePayAlerts")
    root.configure(padx=6, pady=6)
    root.minsize(300, 400)
    root.maxsize(300, 400)

    # window coordinates (center)
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    wx = (sw - root.winfo_reqwidth()) // 2
    wy = (sh - root.winfo_reqheight()) // 2
    root.geometry(f"300x400+{wx}+{wy}")

    # gui
    tabs = ttk.Notebook(root, name="_MAIN_")
    tab1 = ttk.Frame(tabs, name="_TAB1_")
    tab2 = ttk.Frame(tabs, name="_TAB2_")

    tabs.add(tab1, text="General")
    tabs.add(tab2, text="Settings")
    tabs.pack(expand=True, fill="both")

    font_title = ("Arial", 18, "bold")
    font_label = ("Arial", 12, "bold")

    widgets = [
        # Tab 1
        ttk.Separator(tab1),
        ttk.Label(tab1, text="General", font=font_title),
        ttk.Separator(tab1),

        ttk.Button(tab1, text="Start", name="_BTN_START_", command=callback("_BTN_START_")),
        ttk.Separator(tab1),
        ttk.Button(tab1, text="Stop", name="_BTN_STOP_", command=callback("_BTN_STOP_")),
        ttk.Separator(tab1),
        ttk.Button(tab1, text="Test", name="_BTN_TEST_", command=callback("_BTN_TEST_")),

        ttk.Label(tab1, text="MobilePayAlerts", name="_LABEL_TITLE_", font=font_label),
        ttk.Label(tab1, text="Created by Benjamin Stigsen", name="_LABEL_CREDITS_"),

        # Tab 2
        ttk.Separator(tab2),
        ttk.Label(tab2, text="Donation Settings", font=font_title),

        ttk.Separator(tab2),
        ttk.Label(tab2, text="Default Name:", font=font_label),
        ttk.Entry(tab2, name="_INPUT_NAME_"),

        ttk.Separator(tab2),
        ttk.Label(tab2, text="Default Message:", font=font_label),
        ttk.Entry(tab2, name="_INPUT_MSG_"),

        ttk.Separator(tab2),
        ttk.Button(tab2, text="Save Settings", name="_BTN_SAVE_", command=callback("_BTN_SAVE_")),

        ttk.Separator(tab2),
        ttk.Label(tab2, text="Other Settings", font=font_label),
        ttk.Separator(tab2),
        ttk.Button(tab2, text="Reset", name="_BTN_RESET_", command=callback("_BTN_RESET_")),
        ttk.Separator(tab2),
        ttk.Button(tab2, text="Setup", name="_BTN_SETUP_", command=callback("_BTN_SETUP_")),
    ]

    widget_by_name(2, "_INPUT_NAME_").insert(0, cfg["default_name"])
    widget_by_name(2, "_INPUT_MSG_").insert(0, cfg["default_msg"])

    for widget in widgets:
        if isinstance(widget, ttk.Label) and widget.winfo_name() in ["_LABEL_TITLE_", "_LABEL_CREDITS_"]:
            padding = (100) if (widget.winfo_name() == "_LABEL_TITLE_") else (0)
            widget.pack(side=tk.BOTTOM, pady=(0, padding))

        if isinstance(widget, ttk.Separator):
            widget.pack(pady=5)
        else:
            widget.pack()

    sv_ttk.set_theme("dark")
    root.mainloop()

if __name__ == "__main__":
    main()
