# Python module imports
import datetime as dt
import hashlib
from flask import Flask, request, render_template, Response

# Importing local functions
from block import *
from genesis import create_genesis_block
from newBlock import next_block, add_block
from getBlock import find_records
from checkChain import check_integrity

# Flask declarations
app = Flask(__name__)
response = Response()
response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')

# Initializing blockchain with the genesis block
blockchain = create_genesis_block()
data = []

# Default Landing page of the app
@app.route('/',  methods = ['GET'])
def index():
    return render_template("web.html")

# Get Form input and decide what is to be done with it
@app.route('/', methods = ['POST'])
def parse_request():
    if(request.form.get("name")):
        while len(data) > 0:
            data.pop()
        data.append(request.form.get("name"))
        data.append(str(dt.date.today()))
        return render_template("webpage.html",
                                name = request.form.get("name"),
                                date = dt.date.today())

    elif(request.form.get("number")):
        while len(data) > 2:
            data.pop()
        data.append(request.form.get("course"))
        data.append(request.form.get("year"))
        return render_template("webattendance.html",
                                name = data[0],
                                course = request.form.get("course"),
                                year = request.form.get("year"),
                                number = int(request.form.get("number")))
    elif(request.form.get("roll_no1")):
        while len(data) > 4:
            data.pop()
        return render_template("webresult.html", result = add_block(request.form, data, blockchain))

    else:
        return "Invalid POST request. This incident has been recorded."

# Show page to get information for fetching records
@app.route('/webresult.html',  methods = ['GET'])
def view():
    return render_template("webpage.html")

# Process form input for fetching records from the blockchain
@app.route('/webresult.html',  methods = ['POST'])
def show_records():
    data = []
    data = find_records(request.form, blockchain)
    if data == -1:
        return "Records not found"
    return render_template("webresult.html",
                            name = request.form.get("name"),
                            course = request.form.get("course"),
                            year = request.form.get("year"),
                            status = data,
                            number = int(request.form.get("number")),
                            date = request.form.get("date"))

# Show page with result of checking blockchain integrity
@app.route('/webresult.html',  methods = ['GET'])
def check():
    return render_template("webresult.html", result = check_integrity(blockchain))

# Start the flask app when program is executed
if __name__ == "__main__":
    app.run()
