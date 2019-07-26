from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB


#tells what db engine to communicate with
engine = create_engine('sqlite:///restaurantmenu.db')
# makes connect between class definitions and coresponding tables with in db
Base.metadata.bind = engine
#link of communications between code excution and engine we created.
#changes to database or made via dbsession (staging zone until it is commited)
DBSession = sessionmaker(bind=engine)
session =DBSession()





class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                output += "<a href='restaurants/new'>Make a New Restaurant Here</a> "
                for restaurant in restaurants:
                    output += restaurant.name
                    output += '</br>' "<a href='/restaurants/%s/edit'>edit</a>" %restaurant.id
                    output += "<a href= '/restaurants/%s/delete' >delete</a>" %restaurant.id
                    output += "</br></br>"

                    output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value= 'Rename'>"
                    output += "</form>"
                    output +="</body></html>"

                    self.wfile.write(output)

                    #output += resturant.name
                    #output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'+restaurant.id +'/edit'><h2>rename</h2><input name="edit rest" type="text" ><input type="submit" value="edit"> </form>'''

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += "are you sure you want to delete %s " % myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurantIDPath
                    #output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value= 'delete'>"
                    output += "</form>"
                    output +="</body></html>"

                    self.wfile.write(output)

            if self.path.endswith("restaurants/new"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                #output += "<div>"
                #output += "<label for='msg'>Restaurant name:</label>"
                #output += "<textarea id='msg' name='user_message'></textarea>"
                #output += "</div>"
                #output += "<div>"
                #output += "<div class='button'>"
                #output += "<button type='Create'>Create a restaurant</button>"
                #output += "</div>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>enter a new restaurant name!</h2><input name="new rest" type="text" ><input type="submit" value="Create"> </form>'''

                output += "</body></html>"
                self.wfile.write(output)

                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:

                if self.path.endswith("/delete"):
                    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    #if ctype == 'multipart/form-data':
                    #    fields = cgi.parse_multipart(self.rfile, pdict)
                    #    messagecontent= fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()

                    if myRestaurantQuery != []:
                        session.delete(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()



                if self.path.endswith("/edit"):
                    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent= fields.get('newRestaurantName')
                        restaurantIDPath = self.path.split("/")[2]

                        myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()

                        if myRestaurantQuery != []:
                            myRestaurantQuery.name = messagecontent[0]
                            session.add(myRestaurantQuery)
                            session.commit()
                            self.send_response(301)
                            self.send_header('Content-type', 'text/html')
                            self.send_header('Location', '/restaurants')
                            self.end_headers()




                if self.path.endswith("/restaurants/new"):
                    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent= fields.get( 'new rest')
                    newRes = Restaurant(name = messagecontent[0])
                    session.add(newRes)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants/new')
                    self.end_headers()
                    return


        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
