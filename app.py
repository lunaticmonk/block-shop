from flask import Flask, request, render_template,redirect,url_for
from pymongo import MongoClient
import time

app = Flask(__name__)

CONNECTION = 'mongodb://blockshop:blockshop@ds113445.mlab.com:13445/blockshop'
client = MongoClient(CONNECTION)
db = client.blockshop
TRANSACTION_LIMIT = 2
ORDER_ID = 1000



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
        self.verified = 0


    def addBlock(self):
        print 'adding block...'
        index = db.blockchain.count()
        timestamp = time.time()
        db.blockchain.insert_one({ 'transactions': self.transactions, 'index': index, 'timestamp': timestamp})
        self.transactions = []

    def add_transaction(self, userid, vehicle_no, address):
        global ORDER_ID
        if (len(self.transactions)< TRANSACTION_LIMIT):
            self.transactions.append({ 'order_id':ORDER_ID,'userid': userid, 'vehicle_no': vehicle_no, 'address': address, 'features': None, 'review':[]})
            ORDER_ID += 1
        else:
            print 'Please Wait'

# global vars

currentblock = currentBlock()

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    # self.currentBlock = currentBlock()
    return render_template('index.html', current_trans= currentblock.transactions), 200
    # return 'success', 200

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        tobereviewed = []
        for item in currentblock.transactions:
            if item['features'] is not None:
                tobereviewed.append(item)
            else:
                return render_template('survey.html', order_id=request.args.get('id'))

        return render_template('review.html', tobereviewed = tobereviewed)
    if request.method == 'POST':
        order_id = request.form['order_id']
        features = {'ABS':request.form['abs'],'power_steering':request.form['powersteering'], 'power_window': request.form['powerwindow'], 'ac': request.form['ac']}
        for i,item in enumerate(currentblock.transactions):
            if str(item['order_id']) == str(order_id):
                currentblock.transactions[i]['features']= features
                currentblock.verified += 1
        if currentblock.verified == TRANSACTION_LIMIT:
            currentblock.addBlock()
        return redirect(url_for('index'))

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
