from flask import Flask, request,jsonify
from bson.binary import Binary

from pymongo import MongoClient 

from flask_cors import CORS
import json





app = Flask(__name__)


import firebase_admin
from firebase_admin import credentials,firestore
import firebase_admin.db as fb_db



# import psycopg2

# conn = psycopg2.connect(
#     host="localhost",
#     database="cart",
#     user="dev",
#     password="0000"
# )

# conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)


# cur = conn.cursor()

# create table if it doesn't exist

def find_product_with_same_cart_product_id(pr_id,data):
        for e in data :
            if e['id']== pr_id :
                return e
        return None



def list_without_null(list):
    list = [x for x in list if x!=None]
    return list 

def get_correct_data(data):
    if data != None : 
        if type(data) == type([]):
            return list_without_null(data)
        else : 
            return list_without_null(list(data.values()))
    else : 
        return []





if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")






cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://prodcut-f9355-default-rtdb.firebaseio.com/'
})



@app.route('/buy',methods=['POST'])
def buy():
    try : 
        cart_data = get_correct_data(fb_db.reference('cart').get()) 
        if len(cart_data):
            product_data = get_correct_data(fb_db.reference('products').get())
            updated = []
            for cart_product in cart_data : 
                print("cart_product : ",cart_product)
                print("\n")
                cart_product_id = cart_product['id']
                cart_product_quantity = cart_product['quantity']
                product_record = find_product_with_same_cart_product_id(cart_product_id,product_data)
                cart_product_flavor = cart_product['flavor']
                print("cart_product_flavor ",cart_product_flavor)
                print("\n")
                record_pieces = product_record['flavor'].get(cart_product_flavor)
                if record_pieces>= cart_product_quantity : 
                    updated.append((
                        product_record['name'],True
                    ))
                    print("cart_product_quantity",cart_product_quantity)
                    print("\n")
                    new_record_pieces=record_pieces - cart_product_quantity
                    print("old product record  : ",product_record)
                    print("\n")
                    print("new record pieces : ",new_record_pieces)
                    product_record['flavor'][cart_product_flavor] = new_record_pieces
                    print("new_product_record : ",product_record)
                    print("\n")
                    record_id = product_record['id']
                    record_ref = fb_db.reference('products/' + str(record_id)) 
                    print("product record that is going to be send to firebase : ",product_record)
                    print("\n")
                    record_ref.update(product_record)
                    cart_data_=fb_db.reference('cart/'+str(record_id))
                    cart_data_.delete()
                else : 
                    updated.append((
                        product_record['name'],False
                    ))
            client_message = []
            for up in updated :
                if up[1]:
                    client_message.append("succeful buy for : "+up[0])
                else : 
                    client_message.append("not enough pieces for : "+up[0])
            print(client_message)
            return client_message
        else : 
            return "empty"

    except Exception as e:
        return jsonify({'error': str(e)}), 500







@app.route('/data', methods=['GET'])
def get_data():
    try:
        print('were in ')
        ref = fb_db.reference('cart')
        data = ref.get()
        return get_correct_data(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/products', methods=['GET'])
def get_products():
    try:
        ref = fb_db.reference('products')
        data = ref.get()
        return get_correct_data(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# define endpoint to add data to database
@app.route('/data', methods=['POST'])
def add_data():
    try:
        cart_ref = fb_db.reference('cart')
        data = request.get_json()
        id = data['id']
        quantity = data['quantity']
        flavor = data['flavor']
        send = {
            'id':id,
            'quantity' : quantity,
            'flavor':flavor
        }
        cart_ref.child(str(id)).set(data)
        return jsonify({'message': 'Data added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500






