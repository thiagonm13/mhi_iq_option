import json
import time
from configuration import getConfig, getAccount
from mhi import MHI

while True:
	config_mhi = getConfig()
	if config_mhi['estado'] == True:
		account = getAccount()
		compra = MHI( account['email'], account['password'] )
		compra.start()
	time.sleep(0.5)