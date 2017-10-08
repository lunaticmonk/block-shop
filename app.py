from flask import Flask, request, render_template,redirect,url_for
from pymongo import MongoClient
import time

app = Flask(__name__)

CONNECTION = 'mongodb://blockshop:blockshop@ds113445.mlab.com:13445/blockshop'
client = MongoClient(CONNECTION)
db = client.blockshop
TRANSACTION_LIMIT = 2
ORDER_ID = 1000
REVIEW_REQUIRED = 2

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

    def add_transaction(self, trans):
        self.transactions.append(trans)
        del current_transactions.transaction_dict[trans.order_id]
        if len(self.transactions) == TRANSACTION_LIMIT:
            self.addBlock()


class current_Transactions(object):
    def __init__(self):
        self.transaction_dict = {}

    def add_transaction(self,ORDER_ID,transaction):
        self.transaction_dict[ORDER_ID] = transaction

    # def remove_trans(self,order_id):
    #     print 'removing'
    #     print type(order_id)
    #     del current_transactions.transaction_dict[int(order_id)]
    #     print 'removed'

class Transaction(object):
    def __init__(self,user_id,vehicle_no,address):
        global ORDER_ID
        self.order_id = ORDER_ID
        self.seller_id = user_id
        self.vehicle_no = vehicle_no
        self.address = address
        self.features = None
        # self.review_by = []
        self.review_no = 0
        self.verified = False
        ORDER_ID += 1

    def check_verification(self):
        if self.review_no == REVIEW_REQUIRED:
            print 'equaled'
            self.verified = True
            currentblock.add_transaction(self)
            del current_transactions.transaction_dict[int(self.order_id)]
        else:
            pass

    def review_true(self):
        # self.review_by.append(user_id)
        self.review_no += 1
        self.check_verification()

    def review_false(self):
        self.features = None
        self.review_no = 0

    def add_feature(self,features):
        self.features = features

    def __str__(self):
        return str([self.order_id,self.vehicle_no,self.address])

# global vars

currentblock = currentBlock()
current_transactions = current_Transactions()

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    # self.currentBlock = currentBlock()
    return render_template('index.html', current_trans= current_transactions.transaction_dict), 200
    # return 'success', 200

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        transaction = current_transactions.transaction_dict[int(request.args.get('id'))]
        if transaction.features is not None:
            return render_template('review.html', trans = transaction )
        else:
            return render_template('survey.html', order_id=request.args.get('id'))

    if request.method == 'POST':
        order_id = request.form['order_id']
        features = {'ABS':request.form['abs'],'power_steering':request.form['powersteering'], 'power_window': request.form['powerwindow'], 'ac': request.form['ac']}
        current_transactions.transaction_dict[int(order_id)].features = features
        return redirect(url_for('index'))

@app.route('/review/type',methods=['POST'])
def type():
    if request.method == 'POST':
        order_id = request.form['order_id']
        if str(request.form['status'])=='1':
            current_transactions.transaction_dict[int(order_id)].review_true()
        else:
            current_transactions.transaction_dict[int(order_id)].review_false()
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
        temp = Transaction(userid,vehicle_no,address)
        current_transactions.add_transaction(temp.order_id,temp)
        return redirect(url_for('index'))
    return 'new transaction', 200

@app.route('/chain')
def chain():
    return 'full chain', 200

# @app.route('/')

if __name__ == "__main__":
    app.run(debug=True)
