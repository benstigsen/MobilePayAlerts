import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Setting some window properties
root.title("Tk Example")
root.configure(background="yellow")
root.minsize(200, 200)
root.maxsize(500, 500)
root.geometry("300x300+3200+400")

tabs = ttk.Notebook(root)
tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)

tabs.add(tab1, text="General")
tabs.add(tab2, text="Settings")
tabs.pack(expand=True, fill="both")

font_title = font=("Arial", 18, "bold")
font_label = font=("Arial", 12, "bold")

widgets = [
    # Tab 1
    ttk.Separator(tab1),
    ttk.Label(tab1, text="General", font=font_title),
    ttk.Separator(tab1),

    ttk.Button(tab1, text="Start", name="_BTN_START_"),
    ttk.Separator(tab1),
    ttk.Button(tab1, text="Stop", name="_BTN_STOP_"),
    ttk.Separator(tab1),
    ttk.Button(tab1, text="Test", name="_BTN_TEST_"),

    ttk.Separator(tab1),
    ttk.Separator(tab1),
    ttk.Label(tab1, text="MobilePayAlerts", font=font_label),
    ttk.Label(tab1, text="Created by Benjamin Stigsen"),

    # Tab 2
    ttk.Separator(tab1),
    ttk.Label(tab2, text="Donation Settings", font=font_title),

    ttk.Separator(tab2),
    ttk.Label(tab2, text="Default Name:", font=font_label),
    ttk.Entry(tab2, name="_INPUT_NAME_"),

    ttk.Separator(tab2),
    ttk.Label(tab2, text="Default Message:", font=font_label),
    ttk.Entry(tab2, name="_INPUT_MESSAGE_"),

    ttk.Separator(tab2),
    ttk.Button(tab2, text="Save Settings", name="_BTN_SAVE_"),
    ttk.Separator(tab2),

    ttk.Label(tab2, text="Other Settings", font=font_label),
    ttk.Button(tab2, text="Reset", name="_BTN_RESET_"),
    ttk.Button(tab2, text="Setup", name="_BTN_SETUP_"),
]

for widget in widgets:
    if isinstance(widget, ttk.Separator):
        widget.pack(pady=5)
    else:
        widget.pack()

root.mainloop()
