
import json

default = {
  "estado": False,
  "chat_id": 0,
  "operacao": 1,
  "tipo_mhi": 1,
  "par": "",
  "valor_entrada": 2.0,
  "valor_entrada_b": 2.0,
  "martingale": 1,
  "stop_loss": 0,
  "stop_gain": 0,
  "payout": 75
}

def getConfig ():
  config = open('config.json', 'r').read()
  if config.strip() == '':
    with open('config.json', 'w') as old_config:
      json.dump(default, old_config, indent=2)
		
    config = default
  else:
    config = json.loads(config)	
  return config

def setConfig ( data ):
  config = getConfig()
  for conf in data:
    config[conf] = data[conf]
  with open('config.json', 'w') as old_config:
    json.dump( config, old_config, indent=2 )
  
def getAccount():
  account = open( 'account.json', 'r' ).read()
  return json.loads( account )
  