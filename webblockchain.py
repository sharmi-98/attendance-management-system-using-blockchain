# Python module imports
import datetime as dt
from flask import Flask, request, render_template
from newBlock import next_block, add_block
from getBlock import find_records
from checkChain import check_integrity

# Flask declarations
app = Flask(__name__)

# Initializing blockchain with the genesis block
blockchain = create_genesis_block()
data = []

# Default Landing page of the app
@app.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get("name"):
            data.clear()
            data.append(request.form.get("name"))
            data.append(str(dt.date.today()))
            return render_template("webpage.html", name=request.form.get("name"), date=dt.date.today())
        elif request.form.get("number"):
            data.append(request.form.get("course"))
            data.append(request.form.get("year"))
            return render_template("webattendance.html", name=data[0], course=request.form.get("course"), year=request.form.get("year"), number=int(request.form.get("number")))
        elif request.form.get("roll_no1"):
            result = add_block(request.form, data, blockchain)
            return render_template("webresult.html", result=result)
        else:
            return "Invalid POST request. This incident has been recorded."
    else:
        return render_template("web.html")

# Show page to get information for fetching records
@app.route('/webresult.html',  methods=['GET', 'POST'])
def view():
    return render_template("webpage.html")

# Process form input for fetching records from the blockchain
@app.route('/webresult.html',  methods=['POST'])
def show_records():
    data.clear()
    data = find_records(request.form, blockchain)
    if data == -1:
        return "Records not found"
    return render_template("webresult.html", name=request.form.get("name"), course=request.form.get("course"), year=request.form.get("year"), status=data, number=int(request.form.get("number")), date=request.form.get("date"))

# Show page with result of checking blockchain integrity
@app.route('/result.html',  methods=['GET'])
def check():
    result = check_integrity(blockchain)
    return render_template("result.html", result=result)

# Start the flask app when program is executed
if __name__ == "__main__":
    app.run(debug=True)
