from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sports_setup import Base, Catagory, equipment

engine = create_engine('sqlite:///sports.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/')
def catagory():
    catagories = session.query(catagory).all()
    output = ''
    for i in catagories:
        output += i.name
        output += '</br>'
        return "hellop"

@app.route('/catagory/<int:catagory_id>/equipment')
def equipmentItem(catagory_id):
        catagory = session.query(Catagory).filter_by(id = catagory_id).one()
        items = session.query(equipment_item).filter_by(catagory_id = catagory_id)
        return "this is where we see the equipment for a specific catagory "
    #return render_template('menu.html', restaurant=restaurant, items = items, restaurant_id = restaurant_id)




@app.route('/catagory/<int:catagory_id>/new', methods=['GET','POST'])
def newEquipmentItem(catagory_id):

	if request.method == 'POST':
		newItem = equipment_item(name = request.form['name'], description = request.form['description'], price = request.form['price'], catagory_id = catagory_id)
		session.add(newItem)
		session.commit()
        return " this is how we add a new equirement item  to a catagory"
        #return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	#else:
		#return render_template('newmenuitem.html', restaurant_id = restaurant_id)




@app.route('/catagory/<int:catagory_id>/<int:equipment_id>/edit', methods = ['GET', 'POST'])
def editEquipmentItem(catagory_id, equipment_id):
	editedItem = session.query(MenuItem).filter_by(id = equipment_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['name']
		if request.form['price']:
			editedItem.price = request.form['price']
		session.add(editedItem)
		session.commit()
        return " this is how we edit an existing equipment item"

		#return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	#else:

		#return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)



@app.route('/catagory/<int:catagory_id>/<int:equipment_id>/delete', methods = ['GET','POST'])
def deleteEquipmentItem(restaurant_id, menu_id):
	itemToDelete = session.query(equipment_item).filter_by(id = equipment_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
        return " this is how we delete an equipment item"

        #return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	#else:
		#return render_template('deleteconfirmation.html', item = itemToDelete)


#ADD JSON API ENDPOINT HERE
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])




if __name__ == '__main__':
	#app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
