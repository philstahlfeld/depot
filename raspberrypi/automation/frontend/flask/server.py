import flask
app = flask.Flask(__name__)

@app.route('/')
def Index():
  return flask.render_template('base.html', name='Phil')

@app.route('/login/', methods=['GET', 'POST'])
def Login():
  if flask.request.method == 'GET':
    return flask.render_template('login_page.html', 
                                 action=flask.url_for('Login'))
  else:
    return 'Called with POST data'



if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
