from flask import Flask, request, render_template,redirect,url_for
from pymongo import MongoClient
import time

app = Flask(__name__)

CONNECTION = 'mongodb://blockshop:blockshop@ds113445.mlab.com:13445/blockshop'
client = MongoClient(CONNECTION)
db = client.blockshop
TRANSACTION_LIMIT = 1
ORDER_ID = 1000
MIN_REVIEW_REQUIRED = 3



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
        self.generated = 5.00
        self.total = 100
        user_id = 101
        for ele in db.user.find():
            db.user.update({"_id":ele["_id"]},{"user_id":user_id,"currency": 0,"reputation":100})
            user_id += 1

    def intial_distribute(self):
        total_users = db.user.count()
        individual_currency = self.initial/float(total_users)
        for ele in db.user.find():
            new_currency = ele['currency'] + individual_currency
            db.user.update({"_id":ele["_id"]},{"$set":{"currency": new_currency}})

    def distribute_reward(self):
        self.total += self.generated
        # # distribution = TRANSACTION_LIMIT * (MIN_REVIEW_REQUIRED + 1)
        # # individual_addition = float(self.generated) / float(distribution)
        # print individual_addition
        last_block_id = db.blockchain.count()-1
        print last_block_id
        last_block = db.blockchain.find_one({"index":last_block_id})
        distribution = 0
        for ele in last_block['transactions']:
            distribution += len(ele['pos_review_by'])
        individual_addition = float(self.generated)/float(distribution)
        print last_block
        for ele in last_block['transactions']:
            user_list = ele['pos_review_by']
            for user_id in user_list:
                db.user.update({"user_id":int(user_id)},{"$inc":{"currency":individual_addition}})




class currentBlock(object):
    def __init__(self):
        self.transactions = []
        self.last_index = db.blockchain.count()-1

    def addBlock(self):
        print 'adding block...'
        index = db.blockchain.count()
        timestamp = time.time()
        temp = { 'transactions': self.transactions, 'index': index, 'timestamp': timestamp}
        print temp
        db.blockchain.insert_one(temp)
        print "sucessfully added to db"
        currency.distribute_reward()
        self.transactions = []
        self.last_index = index

    def add_transaction(self, trans):
        self.transactions.append({'order_id':trans.order_id,'seller_id':trans.seller_id,'address':trans.address,'pos_review_by':trans.pos_review_by,'neg_review_by':trans.neg_review_by})
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
        self.pos_review_by = []
        self.neg_review_by = []
        self.positive_response = 0
        self.negative_response = 0
        self.verified = False
        ORDER_ID += 1

    def check_verification(self):
        print MIN_REVIEW_REQUIRED
        if (self.positive_response+self.negative_response) >= MIN_REVIEW_REQUIRED:
            print "validation done..."
            if self.positive_response>self.negative_response:
                self.verified = True
                currentblock.add_transaction(self)
            else:
                self.features = None
                self.pos_review_by = []
                self.neg_review_by = []
                self.positive_response = 0
                self.negative_response = 0
                self.verified = False

    def review_true(self,user_id):
        # self.review_by.append(user_id)
        self.positive_response += 1
        self.pos_review_by.append(user_id)
        print "hello"
        self.check_verification()
        print "done"

    def review_false(self,user_id):
        self.negative_response += 1
        self.neg_review_by.append(user_id)
        self.check_verification()

    def add_feature(self,features):
        self.features = features

    def __str__(self):
        return str([self.order_id,self.seller_id,self.positive_response,self.negative_response])


# global vars

currentblock = currentBlock()
current_transactions = current_Transactions()
currency = block_currency()
currency.intial_distribute()

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
        current_transactions.transaction_dict[int(order_id)].pos_review_by.append(feature_user_id)
        current_transactions.transaction_dict[int(order_id)].positive_response += 1
        current_transactions.transaction_dict[int(order_id)].check_verification()
        return redirect(url_for('index'))

@app.route('/review/type',methods=['POST'])
def type():
    if request.method == 'POST':
        order_id = request.form['order_id']
        user_id = request.form['user_id']
        if str(request.form['status'])=='1':
            current_transactions.transaction_dict[int(order_id)].review_true(user_id)
        else:
            current_transactions.transaction_dict[int(order_id)].review_false(user_id)
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

@app.route('/distribute')
def distribute():
    return 'success',200

@app.route('/current_distribution')
def cur_distribute():
    user_with_distribution = []
    for ele in db.user.find():
        user_with_distribution.append({'user_id':ele['user_id'],'currency':ele['currency'],'reputation':ele['reputation']})
    return render_template('show_distribution.html', distribution=user_with_distribution)
# @app.route('/')

if __name__ == "__main__":
    app.run(debug=True)
