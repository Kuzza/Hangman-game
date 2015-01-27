from bottle import *
from random import choice
from copy import copy

app = Bottle()

word_list = ["amsterdam", "berlin", "london", "madrid", "paris"]
id = 0
games = {}
words = {}

def get_hidden_word(word, letters):
    hw = copy(word)
    for l in hw:
        if l not in letters:
            hw = hw.replace(l, ".")
    return hw
    
    
@app.route('/games', method='POST')
def start():
    global id
    id += 1
    word = choice(word_list) 
    guessing_word = "."*len(word)
    guessed_letters = []   
    
    games[id] = {'tries_left': 11, 
                 'status': 'busy',
                 'guessing_word': guessing_word,
                 'guessing_letters': guessed_letters
                 }
    words[id] = word
    return '''
    <p>New Hagman game!!<p><br>
    <p>Word to guess:   %s</p>
    <form action='games/%s' method='get'>
    <input value="Try to guess the word!" type="submit">
    </form>
    
    '''    %(guessing_word, id)

@app.route('/games', method='GET')
def overview():
    return '''
        <p>Games: %s</p>
        <form action="/games" method="post">
            <input value="Start Hangman Game now!" type="submit" />
        </form>
        <p>
    '''  %games

@app.route('/games/<id>', method='GET')
def guess(id):
    id = int(id)
    game = games[id]
    guessing_word = game["guessing_word"]
    return '''    
        <p>Game: %s</p>
        <form action="/games/%s" method="post">
            <p>Word to guess:   %s</p>
            <input type="text" name="char" />
            <input value="Guess" type="submit" />
        </form>
        <p>
    '''  %(game, id, guessing_word)


@app.route('/games/<id>', method='POST')
def play(id):  
    id = int(id)
    char = request.forms.get('char')
    game = games[id]
    word = words[id]
    letters = game['guessing_letters']
    if len(char) == 1:
        if char not in letters:
            letters.append(char)    
        if char in word:
            game['guessing_word'] = get_hidden_word(word, letters)
            if "." not in word:
                status =  'success!!!'
        else:
            game['tries_left'] -= 1
            if game['tries_left'] == 0:
                game['status'] = 'failed!!!' 
                return "GAME %s OVER!" %id
            
    return '''    
        <p>Game: %s</p>
        <form action="/games/%s" method="post">
            <p>Word to guess:   %s</p>
            <input type="text" name="char" />
            <input value="Guess" type="submit" />
        </form>
        <p>
    '''  %(game, id, game['guessing_word'])            
        
    

run(app, host='localhost', port=8080) 
