from flask import Flask, render_template, request
import datetime
import hashlib
import json

app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            json.dumps({
                "index": self.index,
                "timestamp": str(self.timestamp),
                "data": self.data,
                "previous_hash": self.previous_hash
            }, sort_keys=True).encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), {"message": "Genesis Block"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

attendance_chain = Blockchain()

@app.route('/')
def index():
    return render_template('web.html')

@app.route('/webattendance', methods=['POST'])
def submit_attendance():
    date = request.form['date']
    roll_number = request.form['roll_number']
    status = request.form['status']

    new_block = Block(len(attendance_chain.chain), datetime.datetime.now(), {"date": date, "roll_number": roll_number, "status": status}, attendance_chain.get_latest_block().hash)
    attendance_chain.add_block(new_block)

    return "Attendance recorded successfully!"

@app.route('/webresult')
def view_attendance():
    return render_template('attendance.html', blockchain=attendance_chain.chain)

if __name__ == '__main__':
    app.run(debug=True)
