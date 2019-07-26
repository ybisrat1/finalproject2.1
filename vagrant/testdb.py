from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind= engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
myFirstRestaurant = Restaurant(name = "pizza palace")
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()

items = session.query(Restaurant).all()
for item in items:
    print (item.name)

