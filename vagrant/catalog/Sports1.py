from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Sports_setup import Catagory, Base, equipment

engine = create_engine('sqlite:///sport.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#adding 1st sport catagory and item
catagory1 = Catagory(name = "football")

session.add(catagory1)
session.commit()

equipment_item1 = equipment(name = "foot ball", description = "pigskin", price = "$5.00", catagory = catagory1)

session.add(equipment_item1)
session.commit()




print ("added equipments items!")
