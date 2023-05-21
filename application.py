from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://prodcut-f9355-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)


def find_product_with_same_cart_product_id(pr_id, data):
    for e in data:
        if e['id'] == pr_id:
            return e
    return None


def list_without_null(lst):
    lst = [x for x in lst if x is not None]
    return lst


def get_correct_data(data):
    if data is not None:
        if isinstance(data, list):
            return list_without_null(data)
        else:
            return list_without_null(list(data.values()))
    else:
        return []


@app.route('/buy', methods=['POST'])
def buy():
    try:
        cart_data = get_correct_data(db.reference('cart').get())
        if len(cart_data):
            product_data = get_correct_data(db.reference('products').get())
            updated = []
            for cart_product in cart_data:
                print("cart_product: ", cart_product)
                print("\n")
                cart_product_id = cart_product['id']
                cart_product_quantity = cart_product['quantity']
                product_record = find_product_with_same_cart_product_id(cart_product_id, product_data)
                cart_product_flavor = cart_product['flavor']
                print("cart_product_flavor: ", cart_product_flavor)
                print("\n")
                record_pieces = product_record['flavor'].get(cart_product_flavor)
                if record_pieces >= cart_product_quantity:
                    updated.append((
                        product_record['name'], True
                    ))
                    print("cart_product_quantity: ", cart_product_quantity)
                    print("\n")
                    new_record_pieces = record_pieces - cart_product_quantity
                    print("old product record: ", product_record)
                    print("\n")
                    print("new record pieces: ", new_record_pieces)
                    product_record['flavor'][cart_product_flavor] = new_record_pieces
                    print("new_product_record: ", product_record)
                    print("\n")
                    record_id = product_record['id']
                    record_ref = db.reference('products/' + str(record_id))
                    print("product record that is going to be sent to firebase: ", product_record)
                    print("\n")
                    record_ref.update(product_record)
                    cart_data_ = db.reference('cart/' + str(record_id))
                    cart_data_.delete()
                else:
                    updated.append((
                        product_record['name'], False
                    ))
            client_message = []
            for up in updated:
                if up[1]:
                    client_message.append("successful buy for: " + up[0])
                else:
                    client_message.append("not enough pieces for: " + up[0])
            print(client_message)
            return jsonify(client_message)
        else:
            return "empty"

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/data', methods=['GET'])
def get_data():
    try:
        print('we\'re in')
        ref = db.reference('cart')
        data = ref.get()
        return jsonify(get_correct_data(data))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/products', methods=['GET'])
def get_products():
    try:
        ref = db.reference('products')
        data = ref.get()
        return jsonify(get_correct_data(data))
    except Exception as e:
