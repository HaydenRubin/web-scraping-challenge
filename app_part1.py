from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

    mars_dict = mongo.mars_app.collection.find_one()

    return render_template("index.html", dict=mars_dict)


@app.route("/scrape")
def scrape():

    # Run the scrape function:
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert = True
    mongo.mars_app.collection.update({}, mars_data, upsert = True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)