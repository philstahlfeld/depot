# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

import flask
import flask_googlelogin
import flask_login
import secrets
import socket
from OpenSSL import SSL
import time

from depot.automation.communication import message
from depot.automation.communication import action_message
from depot.automation.communication import services_message
from depot.automation.communication import status_message
from depot.automation.controllers import services
from depot.automation.controllers import thermostat_service
from depot.media.music.pandora.pianobar import radio_info
from depot.media.music.pandora.pianobar import remote

users = {}

AUTHORIZED = [
    '113044271927424517470',
    '112877179519925844215',
]
BOARDS = {
    'The Birdhouse': '10.1.10.16',
}

action_mapper = {
    services.SWITCHABLE.name: services.SWITCHABLE,
    thermostat_service.THERMOSTAT.name: thermostat_service.THERMOSTAT,
}

app = flask.Flask(__name__)
app.config.update(**secrets.SECRETS)
gl = flask_googlelogin.GoogleLogin(app)


class User(flask_login.UserMixin):

  def __init__(self, userinfo):
    self.id = userinfo['id']
    self.name = userinfo['name']


@gl.user_loader
def GetUser(userid):
  return users.get(userid)


@app.route('/oauth2callback')
@gl.oauth2callback
def Login(token, userinfo, **kwargs):
  user = users[userinfo['id']] = User(userinfo)
  if user.id in AUTHORIZED:
    flask_login.login_user(user)

  return flask.redirect(flask.url_for('Index'))


@app.route('/logout')
def Logout():
  flask_login.logout_user()
  return flask.redirect(flask.url_for('Index'))


@app.route('/')
@flask_login.login_required
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
@flask_login.login_required
def ServicesControl():
  data = flask.request.form
  action_type = action_mapper[data['flavor']]

  if action_type == services.SWITCHABLE:
    msg = action_message.ActionMessage(service_name=data['service_name'],
                                       action=services.OutletService.Toggle)
    s = GetSocket(data['board'])
    msg.SendOverSocket(s)
    s.close()

  elif action_type == thermostat_service.THERMOSTAT:
    msg = action_message.ActionMessage(service_name=data['service_name'],
                                       action=thermostat_service.Thermostat.SetTarget,
                                       target=int(data['target']))
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
    time.sleep(0.25)
  
  render_data = {
      'radio_info': info,
      'radio_action_url': flask.url_for('RadioControl')
  }
  
  return flask.render_template('radio.html', **render_data)

@app.route('/radio_control', methods=['POST'])
@flask_login.login_required
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


if __name__ == '__main__':
  context = SSL.Context(SSL.SSLv23_METHOD)
  context.use_privatekey_file('/home/philstahlfeld/private.pem')
  context.use_certificate_file('/home/philstahlfeld/cert.pem')
  app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
