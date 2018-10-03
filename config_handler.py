import configparser

def __init__(_file):
	cfg = configparser.ConfigParser()
	cfg.read(_file)

	return cfg

def resetSettings(_file):
	cfg = __init__(_file)

	cfg["Main"] = {"language":"english"}
	cfg["GUI"] = {
		"main_bg"		:"#666666",
		"win_bg"		:"#444444",
		"tab"			:"#888888",
		"tab_now"		:"#AAAAAA",
		"tab_txt"		:"#DDDDDD",
		"dropdwn"		:"#555555",
		"dropdwn_txt"	:"#DDDDDD",
		"btn"			:"#666666",
		"btn_txt"		:"#FFFFFF",
		"txt"			:"#DDDDDD",
		"line"			:"#555555"}
	cfg["Donation"] = {
		"default_name"		:"Anon",
		"default_msg"		:""}
	cfg["Credentials"] = {
		"sl_token":cfg.get("Credentials","sl_token").strip(),
		"pb_token":cfg.get("Credentials","pb_token").strip()}

	with open("settings.ini", "w") as cfg_file:
		cfg.write(cfg_file)
