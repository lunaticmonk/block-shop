from flask import Flask, request, render_template,redirect,url_for
from pymongo import MongoClient
import time

app = Flask(__name__)

CONNECTION = 'mongodb://blockshop:blockshop@ds113445.mlab.com:13445/blockshop'
client = MongoClient(CONNECTION)
db = client.blockshop
TRANSACTION_LIMIT = 2


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
        self.index = db.blockchain.count()
        self.transactions = []


    def addBlock(self):
        print 'adding block...'
        index = db.blockchain.count()
        timestamp = time.time()
        db.blockchain.insert_one({ 'transactions': self.transactions, 'index': index, 'timestamp': timestamp})
        self.transactions = []

    def add_transaction(self, userid, vehicle_no, address):
        if (len(self.transactions)< TRANSACTION_LIMIT):
            self.transactions.append({ 'userid': userid, 'vehicle_no': vehicle_no, 'address': address, 'features': None, 'review':[]})
            if (len(self.transactions) == TRANSACTION_LIMIT):
                self.addBlock()
        else:
            print 'limit exceeded..'

# global vars

currentblock = currentBlock()

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    # self.currentBlock = currentBlock()
    return render_template('index.html', current_no= len(currentblock.transactions)), 200
    # return 'success', 200

@app.route('/review', methods=['GET', 'POST'])
def review():
    tobereviewed = []
    for item in currentblock.transactions:
        if item['features'] is not None:
            tobereviewed.append(item)
        else:
            pass
    return render_template('review.html', tobereviewed = tobereviewed)

# @app.route('/review_transaction', methods=['GET', 'POST'])
# def review():
#     for item in currentBlock.transactions

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
        currentblock.add_transaction(userid,vehicle_no,address)
        return redirect(url_for('index'))
    return 'new transaction', 200

@app.route('/chain')
def chain():
    return 'full chain', 200

# @app.route('/')

if __name__ == "__main__":
    app.run(debug=True)
