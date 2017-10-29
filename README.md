# Blockshop
Decentralization of reselling of products with blockchain.

### Hackinout hack
Team Name - The First Man

Project link - [here](https://devpost.com/software/block-shop)

### Inspiration
To make the reselling of things among peers thereby eliminating charges that the merchants charge and also verifying the products with the help of nearby peers of the seller

### What it does
Consider person A is seller and B is buyer.

- A puts a product on the site.
- B wants to buy it. But B wants to eliminate the charges inculcated by the middle merchants like olx or droom.in(in case of automobiles). B also doesn't want to compromise with the quality of the product.
- Thus, we offer a reward( in terms of a currency or ether ) to the peers in the vicinity of the seller A to check the product in person for buyer B.
- The first person( let's say C ) who approaches A records the quality and features of the product and makes a statement whether it is good to buy or not which is to be verified by other peers.
- The following people approaching A after C( say D, E ), counter check the statement of A so as to not have any kind of fraud. They also get a part of generated currency on counter checking the first person's decision so that they won't be without reward.
- If majority of people( minimum 6-7 ) confirm about the quality of product, then we add the transaction and thus many transactions are combined to form a block which we append in our blockchain.
- If a peer tries to fraud, we have a factor called 'Reputation', which would eventually decrease if he tries to do deceit.


### Setup
Create a virtual environment.

```
(for macOS)
virtualenv --python /usr/bin/python2.7 venv
source venv/bin/activate
git clone https://github.com/sumedh123/block-shop
cd block-shop
pip install -r requirements.txt
python app.py
```

Head out to http://localhost:5000 in browser.
