def getLang(lang):
	if lang.lower() == "danish":
		language = {
			# Tab Titles
			"tab_1_title"		:"Generelt",
			"tab_2_title"		:"Indstillinger",
			"tab_3_title"		:"Andet",

			# Buttons
			"btn_apply"			:"Anvend ændringer",
			"btn_reset"			:"Gendan indstillinger",
			"btn_setup"			:"Start MPA opsætning",

			# Buttons Tooltips
			"btn_apply_tt"		:"Anvend nuværende indstillinger",
			"btn_reset_tt"		:"Gendan indstillinger",
			"btn_setup_tt"		:"Start førstegangs opsætning",

			# Messagebox Titles
			"msgbox_apply_t"	:"Genstart MPA",
			"msgbox_setup_0_t"	:"Indstil MPA først",
		}

	if lang.lower() == "english":
		language = {
			# Tab Titles
			"tab_1_title"		:"General",
			"tab_2_title"		:"Settings",
			"tab_3_title"		:"Other",

			# Buttons
			"btn_apply"			:"Apply changes",
			"btn_reset"			:"Restore settings",
			"btn_setup"			:"Start MPA setup",

			# Button Tooltips
			"btn_apply_tt"		:"Apply current settings",
			"btn_reset_tt"		:"Restore settings",
			"btn_setup_tt"		:"Perform first-time setup",

			# Messagebox Titles
			"msgbox_apply_t"	:"Restart MPA",
			"msgbox_setup_0_t"	:"Set up MPA first",
		}

	common = {
		# Window Titles
		"app_main_title"	:"MPA",
		"app_setup_title"	:"MPA - Setup",

		# Buttons
		"btn_start"			:"Start",
		"btn_stop"			:"Stop",
		"btn_test"			:"Test Donation",

		# Button Tooltips
		"btn_start_tt"		:"Start Streamlabs + MobilePay",
		"btn_stop_tt"		:"Stop Streamlabs + MobilePay",
		"btn_test_tt"		:"Test Streamlabs donation",

		# Messagebox
		"msgbox_apply"		:"- Restart MPA to apply changes\n- Genstart MPA for at anvende ændringer",
		"msgbox_setup_0"	:"- Set up MPA first (Go to MPA > Settings > Setup)\n- Indstil MPA først (Gå til MPA > Indstillinger > Andet)",
		"msgbox_setup_1"	:"- Click OK when you want to start setup\n- Vælg OK når du vil starte opsætning",
		"msgbox_setup_2"	:"- Click OK once Pushbullet has been authorized\n- Vælg OK når Pushbullet har fået adgang",
		"msgbox_setup_3"	:"- Click OK once Streamlabs has been authorized\n- Vælg OK når Streamlabs har fået adgang",

		# Labels
		"language"			:"Language/Sprog:",
		"currency"			:"Currency/Valuta:",

		# Dropdown Options
		"language_danish"	:"Danish/Dansk",
		"language_english"	:"English/Engelsk",
	}

	for key, value in common.items():
		language[key] = value

	return language
