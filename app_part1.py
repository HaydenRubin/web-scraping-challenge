from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

 # pymongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Next, create a route called `/scrape` that will import 
# your `scrape_mars.py` script and call your `scrape` 
# function.

# Store the return value in Mongo as a Python dictionary.
@app.route("/scrape")
def scrape():

    # Run the scrape function:
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert = True
    mongo.db.collection.update({}, mars_data, upsert = True)

    # Redirect back to index page. 
    return redirect("/")

# * Create a root route `/` that will query your Mongo 
# database and pass the mars data into an HTML template 
# to display the data.

@app.route("/")
def index():

    destination_data = mongo.db.collection.find_one()

    return render_template("index.html", mars=destination_data)


if __name__ == "__main__":
    app.run(debug=True)