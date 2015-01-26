from bottle import *

app = Bottle()


@app.route('/game', method='POST')
def start():
	return template('Start new game')    

@app.route('/game', method='POST')
def start():
	return template('Start new game') 


@app.route('/rulex/home')
def home():
	return template('main')
