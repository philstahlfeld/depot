import flask
import pdb
import socket

from depot.automation.communication import message
from depot.automation.communication import action_message
from depot.automation.communication import services_message
from depot.automation.communication import status_message
from depot.automation.controllers import services
from depot.media.music.pandora.pianobar import radio_info
from depot.media.music.pandora.pianobar import remote

BOARDS = {
    'The Birdhouse': '10.1.10.18',
}

action_mapper = {
    services.SWITCHABLE.name: services.SWITCHABLE,
}

app = flask.Flask(__name__)

@app.route('/')
def Index():
  render_data = {}
  render_data['radio_path'] = flask.url_for('Radio')
  render_data['radio_action_url'] = flask.url_for('RadioControl')
  render_data['radio_buttons'] = GetPandoraControlBar()

  render_data['services_path'] = flask.url_for('Services')
  render_data['services_action_url'] = flask.url_for('ServicesControl')
  return flask.render_template('base.html', **render_data)

def GetPandoraControlBar():
  radio_buttons = []
  radio_buttons.append({'name': 'Play', 'action': 'play'})
  radio_buttons.append({'name': 'Next', 'action': 'next'})
  radio_buttons.append({'name': '+', 'action': 'volume_up'})
  radio_buttons.append({'name': '-', 'action': 'volume_down'})
  radio_buttons.append({'name': 'Restart', 'action': 'restart'})
  return radio_buttons

def GetSocket(board_name):
  ip = BOARDS[board_name]
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((ip, 14025))
  return s

@app.route('/services')
def Services():
  for board in BOARDS:
    s = GetSocket(board)
    msg = services_message.ServicesMessage()
    msg.SendOverSocket(s)
    msg = message.ReceiveOverSocket(s)
    s.close()
    ds_list = []
    for name in msg.services:
      msg2 = status_message.StatusMessage(name)
      s = GetSocket(board)
      msg2.SendOverSocket(s)
      msg2 = message.ReceiveOverSocket(s)
      s.close()
      ds_list.append(DisplayService(name, msg.services[name].name, msg2.status, board))
  return flask.render_template('services.html', services=ds_list)



class DisplayService(object):

  def __init__(self, name, flavor, status, board):
    self.name = name
    self.flavor = flavor
    self.status = status
    self.board = board

@app.route('/service_control', methods=['POST'])
def ServicesControl():
  data = flask.request.form
  action_type = action_mapper[data['flavor']]

  if action_type == services.SWITCHABLE:
    msg = action_message.ActionMessage(service_name=data['service_name'],
                                       action=services.OutletService.Toggle)
    s = GetSocket(data['board'])
    msg.SendOverSocket(s)
    s.close()

  return 'Success'

@app.route('/radio')
def Radio():
  remote.Start()
  while True:
    info = radio_info.GetCurrentRadioInfo()
    if info:
      break
  
  render_data = {
      'radio_info': info,
      'radio_action_url': flask.url_for('RadioControl')
  }
  
  return flask.render_template('radio.html', **render_data)

@app.route('/radio_control', methods=['POST'])
def RadioControl():
  data = flask.request.form
  if data['action'] == 'play':
    remote.Play()
  elif data['action'] == 'next':
    remote.Next()
  elif data['action'] == 'volume_up':
    remote.VolumeUp()
  elif data['action'] == 'volume_down':
    remote.VolumeDown()
  elif data['action'] == 'restart':
    remote.Stop()
    remote.Start()
  elif data['action'] == 'change_station':
    remote.ChangeStation(data['selector'])
  return 'success'


@app.route('/login/', methods=['GET', 'POST'])
def Login():
  if flask.request.method == 'GET':
    return flask.render_template('login_page.html', 
                                 action=flask.url_for('Login'))
  else:
    return 'Called with POST data'



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
