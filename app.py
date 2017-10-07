from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

CONNECTION = 'mongodb://blockshop:blockshop@ds113445.mlab.com:13445/blockshop'
client = MongoClient(CONNECTION)
db = client.blockshop

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'success', 200

@app.route('/mine', methods=['GET', 'POST'])
def mine():
    return 'mine here', 200

@app.route('/transactions/new', methods=['POSR'])
def newTransaction():
    """
        Saving to mongoDB takes place here.
    """
    return 'new transaction', 200

# @app.route('/')

if __name__ == "__main__":
    app.run(debug=True)
