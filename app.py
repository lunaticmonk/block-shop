from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'success', 200
#
# @app.route('/makeNode', methods=['GET', 'POST'])
# def makeNode():
#     return 'make node', 200
#
# @app.route('/')

if __name__ == "__main__":
    app.run(debug=True)
