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

class user(object):
    def __init__(self):
        self.user_id = 0
        self.currency = 0


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

class block_currency(object):
    def __init__(self):
        self.initial = 100
        self.total = 100

    def create_currency(self):
        self.generated = 5
        self.total = self.initial + self.generated

    def distribute(self):
        pass

class currentBlock(object):
    def __init__(self):
        self.transactions = []

    def addBlock(self):
        print 'adding block...'
        index = db.blockchain.count()
        timestamp = time.time()
        temp = { 'transactions': self.transactions, 'index': index, 'timestamp': timestamp}
        print temp
        db.blockchain.insert_one(temp)
        print "sucessfully added to db"
        currency.create_currency()
        self.transactions = []

    def add_transaction(self, trans):
        self.transactions.append({'order_id':trans.order_id,'seller_id':trans.seller_id,'address':trans.address,'review_by':trans.review_by})
        print self.transactions
        del current_transactions.transaction_dict[trans.order_id]
        if len(self.transactions) == TRANSACTION_LIMIT:
            self.addBlock()


class current_Transactions(object):
    def __init__(self):
        self.transaction_dict = {}

    def add_transaction(self,ORDER_ID,transaction):
        self.transaction_dict[ORDER_ID] = transaction


class Transaction(object):
    def __init__(self,user_id,vehicle_no,address):
        global ORDER_ID
        self.order_id = ORDER_ID
        self.seller_id = user_id
        self.vehicle_no = vehicle_no
        self.address = address
        self.features = None
        self.review_by = []
        self.review_no = 0
        self.verified = False
        ORDER_ID += 1

    def check_verification(self):
        if self.review_no == REVIEW_REQUIRED:
            self.verified = True
            currentblock.add_transaction(self)
        else:
            pass

    def review_true(self,user_id):
        # self.review_by.append(user_id)
        self.review_no += 1
        self.review_by.append(user_id)
        self.check_verification()

    def review_false(self):
        self.features = None
        self.review_no = 0
        self.review_by = []

    def add_feature(self,features):
        self.features = features

    def __str__(self):
        return str([self.order_id,self.seller_id,self.address])


# global vars

currentblock = currentBlock()
current_transactions = current_Transactions()
currency = block_currency()

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
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
        feature_user_id = request.form['user_id']
        features = {'ABS':request.form['abs'],'power_steering':request.form['powersteering'], 'power_window': request.form['powerwindow'], 'ac': request.form['ac']}
        current_transactions.transaction_dict[int(order_id)].features = features
        current_transactions.transaction_dict[int(order_id)].review_by.append(feature_user_id)
        return redirect(url_for('index'))

@app.route('/review/type',methods=['POST'])
def type():
    if request.method == 'POST':
        order_id = request.form['order_id']
        user_id = request.form['user_id']
        if str(request.form['status'])=='1':
            current_transactions.transaction_dict[int(order_id)].review_true(user_id)
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
