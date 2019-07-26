from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sports_setup import Base, Catagory, equipment
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Cata Application"

engine = create_engine('sqlite:///sport.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# page 1 homepage that list all catagories

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login3.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('catagory'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
def catagory():
    catagories = session.query(Catagory).all()
    return render_template('catagories.html', catagories= catagories)

# page 2 add new catagory
@app.route('/catagory/new' , methods = ['GET', 'POST'])
def addcatagory():
    if 'username' not in login_session:
            return redirect('/login')
    if request.method == 'POST':
        #if request.form['name']:
        newItem = Catagory(name = request.form['name'])
        session.add(newItem)
        session.commit()
        flash("catagory added")
        return redirect(url_for('catagory'))


    else:
        return render_template('addCata.html')

# page 3 delete a catagory
@app.route('/catagory/<int:catagory_id>/delete', methods = ['GET', 'POST'])
def deletecatagory(catagory_id):
    if 'username' not in login_session:
            return redirect('/login')
    itemtodelete = session.query(Catagory).filter_by(id =catagory_id).one()
    if request.method == 'POST':
        #itemtodelete = session.query(Catagory).filter_by(id =catagory_id).one()
        session.delete(itemtodelete)
        session.commit()
        flash("catagory deleted")
        return redirect(url_for('catagory'))
    else:
        #itemtodelete = session.query(Catagory).filter_by(id =catagory_id).one()
        return render_template('deleteCata.html', catagory_id = catagory_id, itemtodelete= itemtodelete)
        #catagories =session.query(Catagory).all()
        #itemtodelete = session.query(Catagory).filter_by(id = catagory_id).one()

# page 4 edit a catagory name
@app.route('/catagory/<int:catagory_id>/edit', methods = ['GET', 'POST'])
def editcatagory(catagory_id):
    if 'username' not in login_session:
            return redirect('/login')
    edititem = session.query(Catagory).filter_by(id =catagory_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edititem.name = request.form['name']
        session.add(edititem)
        session.commit()
        flash("catagory edited")
        return redirect(url_for('catagory'))
    else:
        return render_template('editCata.html', catagory_id= catagory_id, e= edititem)

# page 5 list all equipments for a catagory
@app.route('/catagory/<int:catagory_id>/equipment')
def equipmentItem(catagory_id):
        c = session.query(Catagory).filter_by(id = catagory_id).one()
        items = session.query(equipment).filter_by(Catagory_id = catagory_id).all()
        ##eturn "this is where we see the equipment for a specific catagory "
        return render_template('equipment.html',  items = items, catagory_id = catagory_id, c= c)


# page 6 add a new equipment for a catagory
@app.route('/catagory/<int:catagory_id>/new', methods=['GET','POST'])
def newEquipmentItem(catagory_id):
    if 'username' not in login_session:
            return redirect('/login')
    catagory = session.query(Catagory).filter_by(id =catagory_id).one()
    if request.method == 'POST':
        newequip = equipment(name = request.form['name'], description = request.form['description'], price = request.form['price'], Catagory_id = catagory_id)
        session.add(newequip)
        session.commit()
        flash("equipment added")
        return redirect(url_for('equipmentItem', catagory_id = catagory_id))
    else:
        return render_template('addEquip.html', catagory_id = catagory_id, c = catagory)


# page 7 edit an equipment item
@app.route('/catagory/<int:catagory_id>/<int:equipment_id>/edit', methods = ['GET', 'POST'])
def editEquipmentItem(catagory_id, equipment_id):
    if 'username' not in login_session:
            return redirect('/login')
    eitem = session.query(equipment).filter_by(id = equipment_id).one()
    if request.method == 'POST':
        if request.form['name']:
            eitem.name = request.form['name']
        if request.form['description']:
            eitem.description = request.form['description']
        if request.form['price']:
            eitem.price = request.form['price']
        session.add(eitem)
        session.commit()
        flash("equipment edited")
        return redirect(url_for('equipmentItem', catagory_id = catagory_id))
    else:
        return render_template('2editEquipmentitem.html', catagory_id = catagory_id,equipment_id = equipment_id, eitem = eitem)

# page 8 delete an equipment item
@app.route('/catagory/<int:catagory_id>/<int:equipment_id>/delete', methods = ['GET','POST'])
def deleteEquipmentItem(catagory_id, equipment_id):
    if 'username' not in login_session:
            return redirect('/login')
    item = session.query(equipment).filter_by(id = equipment_id ).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("equipment deleted")
        return redirect(url_for('equipmentItem', catagory_id = catagory_id))
    else:

        return render_template('deleteEquip.html', item = item)

#JSON endpoint to pull all the equipment for a catagory
@app.route('/catagory/<int:catagory_id>/JSON')
def catagoryEquipJSON(catagory_id):
    equips = session.query(equipment).filter_by(Catagory_id = catagory_id).all()
    return jsonify(Equipments=[i.serialize for i in equips])




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    #app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
