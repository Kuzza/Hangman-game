from bottle import *
from random import choice
from copy import copy

app = Bottle()

word_list = ["amsterdam", "berlin", "london", "madrid", "paris"]
id = 0
games = {}
words = {}
guessing_letters = {}

overview_tpl = '''
        <p>Games: {{games}}</p>
        <form action="/games" method="post">
            <input value="Start Hangman Game now!" type="submit" />
        </form>
        <p>
        '''

start_tpl = '''
        <p>New Hagman game!!<p><br>
        <p>Word to guess:  {{guessing_word}}</p>
        <form action='games/{{id}}' method='get'>
            <input value="Try to guess the word!" type="submit">
        </form>  
        '''

try_tpl = '''    
        <p>Game: {{game}}</p>
        <form action="/games/{{id}}" method="post">
            <p>Word to guess:   {{guessing_word}}</p>
            <input type="text" name="char" />
            <input value="Guess" type="submit" />
        </form>
        <p>
    ''' 

success_msg = "GAME SUCCESSFULLY FINISHED!!"
failed_msg = "GAME OVER!!"

busy_status = "busy"
success_status = "success"
failed_status = "failed"

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
    games[id] = {"tries_left": 11, 
                 "status": busy_status,
                 "guessing_word": guessing_word,
                 }
    words[id] = word
    guessing_letters[id] = []    
    return template(start_tpl,  guessing_word=guessing_word, id=id)


@app.route('/games', method='GET')
def overview():
    return  template(overview_tpl, games=games)

@app.route('/games/<id>', method='GET')
def guess(id):
    id = int(id)
    game = games[id]
    if game["status"] == success_status:
        return success_msg
    elif game["status"] == failed_status:
        return failed_msg
    guessing_word = game["guessing_word"]
    return template(try_tpl, game=game, id=id, guessing_word=game['guessing_word'])         

@app.route('/games/<id>', method='POST')
def play(id):  
    id = int(id)
    char = request.forms.get('char')
    game = games[id]
    word = words[id]
    letters = guessing_letters[id]
    if len(char) == 1:
        if char not in letters:
            letters.append(char)    
        if char in word:
            game['guessing_word'] = get_hidden_word(word, letters)
            if "." not in game['guessing_word']:
                game['status'] = success_status 
                return success_msg
        else:
            game['tries_left'] -= 1
            if game['tries_left'] == 0:
                game['status'] = failed_status
                return failed_msg
            
    return template(try_tpl, game=game, id=id, guessing_word=game['guessing_word'])            
        
    

run(app, host='localhost', port=8080) 
