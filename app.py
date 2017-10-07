from flask import Flask, request, render_template
from pymongo import MongoClient
import time

app = Flask(__name__)

CONNECTION = 'mongodb://blockshop:blockshop@ds113445.mlab.com:13445/blockshop'
client = MongoClient(CONNECTION)
db = client.blockshop


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        # Creates a new Block and adds it to the chain
        pass

    def new_transaction(self):
        # Adds a new transaction to the list of transactions
        pass

    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass

class currentBlock(object):
    def __init__(self):
        self.numberOfTransaction = 0
        self.index = db.blockchain.count()
        self.transactions = []

    def addBlock(self):
        transactions = self.transactions
        index = db.blockchain.count() + 1
        timestamp = time.time()
        db.blockchain.insert_one({ 'transactions': transactions, 'index': index, 'timestamp': timestamp})


    def add_transaction(self, userid, vehicle_no, address):
        if (self.numberOfTransaction < 5):
            self.transactions.append({ 'userid': userid, 'vehicle_no': vehicle_no, 'address': address})
            self.numberOfTransaction += 1
        else:
            self.addBlock(currentBlock)
# global vars

currentBlock = currentBlock()

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    # self.currentBlock = currentBlock()
    return render_template('index.html'), 200
    # return 'success', 200

@app.route('/mine', methods=['GET', 'POST'])
def mine():
    return 'mine here', 200

# @app.route('/review_transaction', methods=['GET', 'POST'])
# def review():
    # for item in currentBlock.transactions

@app.route('/transactions/new', methods=['GET', 'POST'])
def newTransaction():
    """
        Saving to mongoDB takes place here.
    """
    if request.method == 'GET':
        return render_template('newtransaction.html')
    if request.method == 'POST':
        # print request.form['id']
        userid = request.form['id']
        vehicle_no = request.form['vehicle_no']
        address = request.form['address']
        return render_template('index.html')
    # newT = {
    #     "prop1": 1,
    #     "prop2": 2
    # }
    # db.transaction.insert_one(newT)
    return 'new transaction', 200

@app.route('/chain')
def chain():
    return 'full chain', 200

# @app.route('/')

if __name__ == "__main__":
    app.run(debug=True)
