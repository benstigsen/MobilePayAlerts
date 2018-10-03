import logging

def __init__():
	log = logging.getLogger("output")

	if not log.handlers:
		filelog = logging.FileHandler("output.log")
		formatlog = logging.Formatter("[Line: %(lineno)d | File: %(filename)s | Func: %(funcName)s] [%(asctime)s] [%(levelname)s]: %(message)s")
		filelog.setFormatter(formatlog)
		log.addHandler(filelog)
		log.setLevel(logging.INFO)

	return log
