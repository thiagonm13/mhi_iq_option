
import json
import requests
import time
from threading import Thread, Lock
from commands import setOperation
import commands
from configuration import getConfig, getAccount


global config
token = getAccount()['token']
config = { 
	'url': f'https://api.telegram.org/bot{token}/', 
	'lock': Lock(), 
}

def del_update(data):
	global config	
	
	config['lock'].acquire()
	requests.post(config['url'] + 'getUpdates', {'offset': data['update_id']+1})
	config['lock'].release()

def send_message(data, msg):
	global config
	
	config['lock'].acquire()
	requests.post(config['url'] + 'sendMessage', {'chat_id': data['message']['chat']['id'], 'text': str(msg)})
	config['lock'].release()

def getUpdateResult ():
  result = ''
  while 'result' not in result:
    try:
      result = json.loads(requests.get(config['url'] + 'getUpdates').text)
    except Exception as e:
      result = ''
      if 'Failed to establish a new connection' in str(e):
        print('Perca de conexão')
      else:
        print('Erro desconhecido: ' + str(e))
  return result


all_commands = {
  '/ligar': {
    'description': 'Ligar ou desligar o bot.',
    'callback': commands.turnOnBot
  },
  '/par': {
    'description': 'Digite a paridade que deseja operar',
    'callback': commands.setParity
  },
  '/operacao': {
    'description': 'Digital ou Binario',
    'callback': commands.setOperation 
  },
  '/tipo_mhi': {
    'description': 'Minoria ou maioria',
    'callback': commands.setType
  },
	'/valor_entrada': {
    'description': 'Defina o valor de entrada',
    'callback': commands.setInputValue
  },
	'/martingale': {
    'description': 'Quantos martingales utilizar',
    'callback': commands.setMartingale
  },
	'/stop_loss': {
    'description': 'Valor para Stop Loss',
    'callback': commands.setStopLoss
  }, 
	'/stop_gain': {
    'description': 'Valor para Stop Gain',
    'callback': commands.setStopGain
  },
  '/payout': {
    'description': 'Digite o payout minimo',
    'callback': commands.setPayout
  }
}

def command_start( data ):
  msg = '''
    Bem vindo ao exemplo de MHI via Telegram!.

    Use os comandos abaixo!
  '''

  for command in all_commands:
    msg += f" {command} - {all_commands[command]['description']}\n"
  Thread(target=send_message, args=( data, msg )).start()



while True:
  x = getUpdateResult()
  print('aguardando mensagem!')
  if len(x['result']) > 0:
    for data in x['result']:
      Thread(target=del_update, args=(data, )).start()
      if 'entities' in data['message']:
        if data['message']['entities'][0]['type'] == 'bot_command':
          if '/start' in data['message']['text']:
            command_start(data)
          else:
            for command in all_commands:
              if command in data['message']['text']:
                config_mhi = getConfig()
                callback = all_commands[command]['callback']
                callback( data, send_message, config_mhi )
                break
      else:
        Thread( target=send_message, args=(data, "Desculpa, não sei o que fazer!") ).start()
  time.sleep(0.25)