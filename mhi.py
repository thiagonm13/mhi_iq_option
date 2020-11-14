
from logging import exception
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time
import sys
import configuration


class MHI:

  def __init__(self, email, password):
    self.API = IQ_Option(email, password)
    self.config = configuration.getConfig()
    self.connection()

  def connection(self):
    self.API.connect()
    self.API.change_balance('PRACTICE')

    if self.API.check_connect():
      print(' Conectado com sucesso!')
    else:
      print(' Erro ao conectar')
      sys.exit()

  def stop(self, lucro):
    if lucro <= float(-1*abs(self.config['stop_loss'])):
      print('Stop Loss batido!')
      sys.exit()

    if lucro >= float(abs(self.config['stop_gain'])):
      print('Stop Gain Batido!')
      sys.exit()

  def Martingale(self, valor, payout):
    lucro_esperado = valor * payout
    perca = float(valor)

    while True:
      if round( valor*payout, 2) > round(abs(perca) + lucro_esperado, 2):
        return round( valor, 2 )
        break
      valor += 0.01

      
  def Payout( self, par = '' ):
    if par.strip() != '':
      self.API.subscribe_strike_list(par, 1)
      while True:
        d = self.API.get_digital_current_profit(par, 1)
        if d != False:
          d = round(int(d) / 100, 2)
          break
        time.sleep(1)
      self.API.unsubscribe_strike_list(par, 1)
      return d


  def isTime (self):
    minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
    return True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False

  def getColors(self):
    velas = self.API.get_candles( self.config['par'], 60, 3, time.time())
    retorno = ''

    for i in range( len(velas) ):
      if velas[i]['open'] < velas[i]['close']:
        retorno += 'g'
      elif velas[i]['open'] > velas[i]['close']:
        retorno += 'r' 
      else: 
        retorno += 'd'
    
    return retorno

  def getDirection( self, cores ):
    dir = False
    if cores.count('g') > cores.count('r') and cores.count('d') == 0 : 
      dir = ('put' if self.config['tipo_mhi'] == 1 else 'call')
    if cores.count('r') > cores.count('g') and cores.count('d') == 0 :
      dir = ('call' if self.config['tipo_mhi'] == 1 else 'put')
    return dir

  def buyParity(self, dir):
    if self.config['operacao'] == 1:
      return self.API.buy_digital_spot( 
        self.config['par'], 
        self.config['valor_entrada'], 
        dir, 1
      ) 
    else:
      return self.API.buy(
        self.config['valor_entrada'], 
        self.config['par'], 
        dir, 1
      )

  def finishTrade( self, id ):
    finish = ( True, 0 )
    if self.config['operacao'] == 1:
      finish = self.API.check_win_digital_v2(id)
    else:
      finish = ( True, self.API.check_win_v3(id) )

    return finish

  def startTrade( self, dir, payout ):
    lucro = 0
    print('iniciando trader')
    
    self.config['valor_entrada'] = self.config['valor_entrada_b']
    for i in range( self.config['martingale'] ):
      if i > 2:
        dir = 'put' if dir == 'call' else 'call'

      buy, id = self.buyParity(dir)
      if buy:
        print('Compra efetuada')
        while True:
          try:
            finish, valor = self.finishTrade(id)
            print( finish, valor )
          except:
            finish = True
            valor = 0

          if finish:
            print('Operaçao Finalizada')
            print(f"Valor: {valor}")
            
            valor = valor if valor > 0 else float(-1*abs(self.config['valor_entrada']))
            lucro += round(valor, 2)

            print(f"Lucro: {lucro}")
            self.config['valor_entrada'] = self.Martingale( self.config['valor_entrada'], payout )
            
            self.stop(lucro)
            break
        if valor > 0: break
        
  def start( self ):
    self.config['valor_entrada_b'] = self.config['valor_entrada']
    print("Aguardando o horario.")
    while True:
      horas = self.isTime()
      
      payout = self.Payout( self.config['par'] )
      if payout < (self.config['payout']/100):
        print(f'Payout abaixo do minimo permitido: {payout}')
        break

      if horas:
        cores = self.getColors()
        dir = self.getDirection(cores)

        if dir:
          self.startTrade(dir, payout)
      time.sleep(0.5)
