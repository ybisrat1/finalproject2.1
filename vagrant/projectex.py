from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# decorator that wraps function inside the  app.route function that flask created and will route and envoke the function in the code.
@app.route('/')
@app.route('/hello')
def HelloWorld():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
    return output

# python interperter uses application name of__main__
# if statmenet with main will onlu run if from the python interpreter
if __name__ == '__main__':

    # server will reload it self  when modifiy (debug support) and debugger provided)
    #app.debug = True
    app.run(host='0.0.0.0', port=5000)
    # run the server with the applicaiont
    #  only used from the host machine  and must be publicly available (0.0.0.0)
