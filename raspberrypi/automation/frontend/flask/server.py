import flask

from depot.media.music.pandora.pianobar import radio_info
from depot.media.music.pandora.pianobar import remote

app = flask.Flask(__name__)

@app.route('/')
def Index():
  remote.Start()
  render_data = {}
  render_data['radio_path'] = flask.url_for('Radio')
  render_data['div'] = 'Radio'
  return flask.render_template('base.html', **render_data)

@app.route('/radio')
def Radio():
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
  return flask.redirect(flask.url_for('Index'))


@app.route('/login/', methods=['GET', 'POST'])
def Login():
  if flask.request.method == 'GET':
    return flask.render_template('login_page.html', 
                                 action=flask.url_for('Login'))
  else:
    return 'Called with POST data'



if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
