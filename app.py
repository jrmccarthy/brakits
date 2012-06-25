from flask import Flask, render_template, request, session, escape, redirect, url_for, send_from_directory, Response
from pymongo import Connection
import json


app = Flask(__name__)
app.secret_key = '\xc2\x8f9\x13q\xdb\xfe`\xca)\xdc\xdd\xfc[\xc0t\xc2\x82lL\x05t\x87\x14'
conn = Connection()
db = conn['brakits']

def check_password(username, password):
    user = db['admin'].find_one({'username':username})
    if user:
        if user['password'] == password:
            return True
    return False

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'Not Logged In'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        if check_password(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><label for="username">Username: <input type=text name=username>
            <p><label for="password">Password: <input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/admin/create_user', methods=['GET', 'POST'])
def create_user():
    if not 'username' in session:
        return 'Access Denied'
    if request.method=='POST':
        existing = db['admin'].find_one({'username':request.form['username']})
        if existing:
            return 'Username taken'
        db['admin'].insert({'username':request.form['username'], 'password':request.form['password']})
    admins = [item for item in db['admin'].find()]
    print admins
    return render_template('admin_users.html', admins=admins)


# @app.route('/user/')
# @app.route('/user/<user_id>')
# def user_profile(user_id=None):
#     if user_id:
#         pass
#     return render_template('user_profile.html', name=user_id)

@app.route('/test')
def test():
    return send_from_directory('templates/', 'main.html')

@app.route('/test_ko')
def test():
    return send_from_directory('templates/', 'ko.html')


'''
Most of this app is probably just going to return JSON, and we'll rely on some front-end system to do the real work.
Endpoints we might need include:
    GET  /event/                                        : List of available events
    POST /event/                                        : Create a new event with the specified info

    GET  /event/<event_id>/users/                       : List of users participating in <event_id>
    GET  /event/<event_id>/users/<user_id>/             : Stats/info about a specific user and their place in the event
    POST /event/<event_id>/users/                       : Create a new user/users with the specified info

    GET  /event/<event_id>/teams/                       : List of all teams in the event
    GET  /event/<event_id>/teams/<team_id>/             : Stats/info about a specific team and their place in the event
    POST /event/<event_id>/teams/                       : Create a new team/teams with the specified info
    
    GET  /event/<event_id>/matches/                     : List of all matches and results (including unplayed)
    GET  /event/<event_id>/matches/<match_id>/          : Info about a particular match in the event
    POST /event/<event_id>/matches/                     : Post results of a match or matches
'''
@app.route('/event')
@app.route('/event/')
def event():
    events = [item for item in db['event'].find(sort=[("timestamp", 1)])]
    return Response(json.dumps(events), mimetype='application/json')

@app.route('/matches')
@app.route('/matches/')
def matches():
    matches = [item for item in db['matches'].find(sort=[("_id",1)])]
    return Response(json.dumps(matches), mimetype='application/json')
    # ret = {}
    # for item in matches:
    #     ret[item['_id']]=({'team_1':item['team_1'],
    #                    'team_2':item['team_2'],
    #                    'winner':item['winner'],
    #                    'game_time':item['game_time'],
    #                    'round':item['round'] })
    # return Response(json.dumps(ret), mimetype='application/json')

@app.route('/tourney')
@app.route('/tourney/')
def tourney():
    import brakiter
    admin = False
    if 'username' in session:
        admin = True
    matches = [item for item in db['matches'].find(sort=[("_id",1)])]
    teams = [item for item in db['teams'].find(sort=[("_id",1)])]
    table = brakiter.generate_brackets(teams)
    return render_template('brackets.html', table=table, teams=teams, admin=admin)








if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)