import flask
import pdb
import socket

from depot.automation.communication import message
from depot.automation.communication import services_message
from depot.media.music.pandora.pianobar import radio_info
from depot.media.music.pandora.pianobar import remote

app = flask.Flask(__name__)

@app.route('/')
def Index():
  render_data = {}
  render_data['radio_path'] = flask.url_for('Radio')
  render_data['radio_action_url'] = flask.url_for('RadioControl')
  render_data['radio_buttons'] = GetPandoraControlBar()

  render_data['services_path'] = flask.url_for('Services')
  return flask.render_template('base.html', **render_data)

def GetPandoraControlBar():
  radio_buttons = []
  radio_buttons.append({'name': 'Play', 'action': 'play'})
  radio_buttons.append({'name': 'Next', 'action': 'next'})
  radio_buttons.append({'name': '+', 'action': 'volume_up'})
  radio_buttons.append({'name': '-', 'action': 'volume_down'})
  radio_buttons.append({'name': 'Restart', 'action': 'restart'})
  return radio_buttons

@app.route('/services')
def Services():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('10.1.10.18', 14025))
  msg = services_message.ServicesMessage()
  msg.SendOverSocket(s)
  msg = message.ReceiveOverSocket(s)
  s.close()
  return flask.render_template('services.html', service_dict=msg.services)

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
  app.run(host='0.0.0.0', debug=True)
