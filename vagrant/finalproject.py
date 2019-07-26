from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from flask import Flask, render_template, request, redirect, url_for, jsonify

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/', methods = ['GET', 'POST'])
@app.route('/restaurants', methods = ['GET', 'POST'])
def showRestaurant(restaurant_id, menu_id):
    return "this page will show all my restaurants"


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/new', methods = ['GET', 'POST'])
def newRestaurant(restaurant_id, menu_id):
    return "this page will be for adding a new"


@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id, menu_id):
    return "this page will be for editing restaurant %s" %restaurant_id


@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id, menu_id):
    return "this page will be for deleteing restaurant %s" %restaurant_id


@app.route('/restaurants/<int:restaurant_id>', methods = ['GET', 'POST'])
@app.route('/restaurants/<int:restaurant_id>/menu', methods = ['GET', 'POST'])
def showMenuItem(restaurant_id, menu_id):
    return "This page is  menu for restaurant %s" %restaurant_id



@app.route('/restaurants/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id, menu_id):
    return "This page is for making a new menu item %s for restaurant %s" %menu_id %restaurant_id

@app.route('/restaurants/<int:restaurant_id>/menu/menu_id/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    return "This page is for editing menu item %s" %menu_id

@app.route('/restaurants/<int:restaurant_id>/menu/menu_id/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    return "This page is for deleting menu item %s" %menu_id





if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
