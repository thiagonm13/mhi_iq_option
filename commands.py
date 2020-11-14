from threading import Thread
from configuration import setConfig


def turnOnBot(data, send_message, config):
  estado = False if config['estado'] == True else True
  message = "desativado!" if estado == False else "ativado"
  
  setConfig({ 
    "estado": estado,
    "chat_id": data['message']['chat']['id']
  })

  Thread( target=send_message, args=(data, f"Bot MHI {message}!") ).start()


def setParity( data, send_message, config ):
  text = data['message']['text'].replace('/par', '')
  parity = str(text.upper()).strip()
  
  message = f"Paridade selecionada atualmente é {config['par']}!"
  if text.strip() != '':
    setConfig({ 'par': parity })
    message = f"Paridade alterada para {parity}"
  Thread( target=send_message, args=(data, message) ).start()


def setOperation( data, send_message, config ):
  text = data['message']['text'].replace('/operacao', '')
						
  if text.strip() != '':
    if 'digital' in text:
      setConfig({"operacao": 1})
      Thread(target=send_message, args=(data, "Tipo de Operação alterado para DIGITAL!")).start()
    elif 'bin' in text:
      setConfig({"operacao": 2})
      Thread(target=send_message, args=(data, "Tipo de Operação alterado para BINARIO!")).start()


def setType ( data, send_message, config ):
  text = data['message']['text'].replace('/tipo_mhi', '')
						
  if text.strip() != '':
    if 'minoria' in text:
      setConfig({"tipo_mhi": 1})
      Thread(target=send_message, args=(data, "Tipo de analise alterado para MINORIA!")).start()
    elif 'maioria' in text:
      setConfig({"tipo_mhi": 2})
      Thread(target=send_message, args=(data, "Tipo de analise alterado para MAIORIA!")).start()
  else:
    type = 'MINORIA' if config['tipo_mhi'] == 1 else 'MAIORIA'
    Thread(target=send_message, args=(data, f"Tipo de analise atual está para {type}" )).start()


def setMartingale( data, send_message, config ):
  text = ''
  try:
    text = int(str(data['message']['text']).replace('/martingale', ''))							
  except:
    Thread(target=send_message, args=(data, "Quantia de MARTINGALE invalido!")).start()
  
  if str(text).strip() != '':
    if text <= 0:
      setConfig({"martingale": 1})
      Thread(target=send_message, args=(data, "Quantia de MARTINGALE alterado para 0!")).start()
    else:
      setConfig({"martingale": text+1})
      Thread(target=send_message, args=(data, "Quantia de MARTINGALE alterado para " + str(text) + "!")).start()
  else:
    Thread(target=send_message, args=(data, "Sua quantia de MARTINGALE atual é de " + str(config['martingale']-1) )).start()
    

def setStopLoss( data, send_message, config ):
  text = ''
  try:
    text = abs(float((str(data['message']['text']).replace('/stop_loss', '')).replace(',', '.')))
  except:
    Thread(target=send_message, args=(data, "Valor para Stop Loss invalido!")).start()

  if str(text).strip() != '':
    setConfig({"stop_loss": text})
    Thread(target=send_message, args=(data, "Valor para Stop Loss alterado para $" + str(text) + "!")).start()
    
  else:
    Thread(target=send_message, args=(data, "Seu Valor para Stop Loss atual é de $" + str(config['stop_loss']) )).start()
						


def setStopGain( data, send_message, config ):
  text = ''
  try:
    text = abs(float((str(data['message']['text']).replace('/stop_gain', '')).replace(',', '.')))
  except:
    Thread(target=send_message, args=(data, "Valor para Stop Gain invalido!")).start()
  
  if str(text).strip() != '':
    setConfig({"stop_gain": text})
    Thread(target=send_message, args=(data, "Valor para Stop Gain alterado para $" + str(text) + "!")).start()
  else:
    Thread(target=send_message, args=(data, "Seu Valor para Stop Gain atual é de $" + str(config['stop_gain']) )).start()
						


def setInputValue( data, send_message, config ):
  text = ''
  try:
    text = float((str(data['message']['text']).replace('/valor_entrada', '')).replace(',', '.'))							
  except:
    Thread(target=send_message, args=(data, "Valor de entrada invalido!")).start()
  
  if str(text).strip() != '':
    setConfig({"valor_entrada": text, "valor_entrada_b": text})
    Thread(target=send_message, args=(data, "Valor de entrada alterado para $" + str(text) + "!")).start()
    
  else:
    Thread(target=send_message, args=(data, "Seu valor de entrada atual é de $" + str(config['valor_entrada']) )).start()
					


def setPayout( data, send_message, config ):
  text = ''
  try:
    text = float((str(data['message']['text']).replace('/payout', '')).replace(',', '.'))							
  except:
    Thread(target=send_message, args=(data, "Valor de entrada invalido!")).start()

  if str(text).strip() != '':
    setConfig({"payout": text})
    Thread(target=send_message, args=(data, "Valor do payout alterado para $" + str(text) + "!")).start()
  else:
    Thread(target=send_message, args=(data, "O valor atual do payout é de $" + str(config['/payout']) )).start()