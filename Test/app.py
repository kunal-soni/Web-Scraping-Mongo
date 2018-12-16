from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

@app.route("/")
def index():
    mars = client.MarsDB.mars.find_one()
    print(mars)
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = client.MarsDB.mars 
    mars_data = scrape_mars.scrape()
    print(mars_data)
    mars.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
