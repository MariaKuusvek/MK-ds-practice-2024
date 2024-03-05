import sys
import os

import logging
import threading

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(1, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(2, utils_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc

fraud_detection_result = ''
transaction_verification_result = ''
books_suggestions_result = ''


def greet():
    print("hello")

def fraud_detection_func(creditcard):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudServiceStub(channel)
        # Call the service through the stub object.
        response = stub.FraudLogic(fraud_detection.FraudRequest(creditcardnr=creditcard))

    # Adding the result to the global variable
    global fraud_detection_result
    fraud_detection_result = response.verdict


def transaction_verification_func(itemsL, name, contact, street, city, state, zip, country, ccnr, cvv, expdate):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        response = stub.VerificationLogic(transaction_verification.VerificationRequest(itemsLength=itemsL,
                                                                                       userName = name,
                                                                                       userContact = contact,
                                                                                       street = street,
                                                                                       city = city,
                                                                                       state = state,
                                                                                       zip = zip,
                                                                                       country = country,
                                                                                       creditcardnr = ccnr,
                                                                                       cvv = cvv,
                                                                                       expirationDate = expdate,))
        
    global transaction_verification_result
    transaction_verification_result = response.verdict
        

def books_suggestion_func():
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = suggestions_grpc.SuggestionsServiceStub(channel)
        response = stub.SuggestionsLogic(suggestions.SuggestionsRequest())
    global books_suggestions_result 
    books_suggestions_result = response



# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)

# Define a GET endpoint.
@app.route('/', methods=['GET'])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    # Test the fraud-detection gRPC service.
    response = greet()
    # Return the response.
    return response

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Print request object data
    print("Request Data:", request.json)

    print(len(request.json['items']))

    thread_fraud = threading.Thread(target=fraud_detection_func, args=(request.json['creditCard']['number'],))
    thread_verification = threading.Thread(target=transaction_verification_func, args=(len(request.json['items']),
                                                                                        request.json['user']['name'],
                                                                                        request.json['user']['contact'],
                                                                                        request.json['billingAddress']['street'],
                                                                                        request.json['billingAddress']['city'],
                                                                                        request.json['billingAddress']['state'],
                                                                                        request.json['billingAddress']['zip'],
                                                                                        request.json['billingAddress']['country'],
                                                                                        request.json['creditCard']['number'],
                                                                                        request.json['creditCard']['expirationDate'],
                                                                                        request.json['creditCard']['cvv'],))
    thread_books = threading.Thread(target=books_suggestion_func)

    thread_fraud.start()
    thread_verification.start()
    thread_books.start()

    thread_fraud.join()
    thread_verification.join()
    thread_books.join()

    final_verdict = ''

    if fraud_detection_result != '' and transaction_verification_result != '' and books_suggestions_result != '' :
        if fraud_detection_result == 'Not Fraud' and transaction_verification_result == 'Pass':
            final_verdict = 'Order Approved'
        else:
            final_verdict = 'Order NOT Approved'


    # Dummy response following the provided YAML specification for the bookstore
    order_status_response = {
        'orderId': '12345',
        'status': final_verdict,
        'suggestedBooks': [
            {'bookId': '123', 'title': 'Dummy Book 1', 'author': 'Author 1'},
            {'bookId': '456', 'title': 'Dummy Book 2', 'author': 'Author 2'}
        ]
    }

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
