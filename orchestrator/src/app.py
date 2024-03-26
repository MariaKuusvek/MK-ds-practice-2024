import sys
import os
import threading
import logging
logging.basicConfig(level=logging.DEBUG)

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

response_verdict = ''
response_reason = ''
response_books = ''


def greet():
    print("hello")

def fraud_detection_func(creditcard, userName, userContact):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudServiceStub(channel)
        # Call the service through the stub object.
        response = stub.startFraudDecMicroService(fraud_detection.FraudThreadRequest(creditCardNr=creditcard, userName = userName, userContact = userContact))


def transaction_verification_func(itemsL, name, contact, street, city, state, zip, country, ccnr, cvv, expdate, orderId):
    # Establish a connection with the transaction verification gRPC service.
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        # Create a stub object.
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        # Call the service through the stub object.
        response = stub.startTransVerMicroService(transaction_verification.VerificationThreadRequest(itemsLength=itemsL,
                                                                                                userName = name,
                                                                                                userContact = contact,
                                                                                                street = street,
                                                                                                city = city,
                                                                                                state = state,
                                                                                                zip = zip,
                                                                                                country = country,
                                                                                                creditcardnr = ccnr,
                                                                                                cvv = cvv,
                                                                                                expirationDate = expdate,
                                                                                                orderId = orderId))
        
    # Adding the result to the global variable
    global response_verdict
    global response_reason
    global response_books
    response_verdict = response.verdict
    response_reason = response.reason
    response_books = response.books
        

def books_suggestion_func():
    # Establish a connection with the book suggestions gRPC service.
    with grpc.insecure_channel('suggestions:50053') as channel:
        # Create a stub object.
        stub = suggestions_grpc.SuggestionsServiceStub(channel)
        # Call the service through the stub object.
        response = stub.startBookSuggestionsMicroService(suggestions.SuggestionsThreadRequest())



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

    logging.info('Checkout REST started')
   
    # Print request object data
    print("Request Data:", request.json)

    path = os.getcwd() + "/orchestrator/src/orderId.txt"
    file = open(path, "r+")
    id = file.readline()
    orderId = int(id) + 1
    file.close()

    file = open(path, "w")
    file.write(str(orderId))
    file.close() 

    # Creating threads to call out microservices
    thread_fraud = threading.Thread(target=fraud_detection_func, args=(request.json['creditCard']['number'],
                                                                       request.json['user']['name'],
                                                                       request.json['user']['contact']))
    thread_verification = threading.Thread(target=transaction_verification_func, args=(len(request.json['items']),
                                                                                        request.json['user']['name'],
                                                                                        request.json['user']['contact'],
                                                                                        request.json['billingAddress']['street'],
                                                                                        request.json['billingAddress']['city'],
                                                                                        request.json['billingAddress']['state'],
                                                                                        request.json['billingAddress']['zip'],
                                                                                        request.json['billingAddress']['country'],
                                                                                        request.json['creditCard']['number'],
                                                                                        request.json['creditCard']['cvv'],
                                                                                        request.json['creditCard']['expirationDate'],
                                                                                        orderId))
    thread_books = threading.Thread(target=books_suggestion_func)

    # Starting threads
    thread_fraud.start()
    thread_verification.start()
    thread_books.start()

    logging.info('Threads in orchestrator started')

    # Ending threads
    thread_fraud.join()
    thread_verification.join()
    thread_books.join()

    logging.info('Threads in orchestrator finished')

    order_status_response = {}

    # Creating response based on the results of the microservices
    if response_verdict != '' and response_reason != '' and response_books != '':
        if response_verdict == 'Pass':

            order_status_response = {
                'orderId': orderId,
                'status': 'Order Approved',
                'suggestedBooks': response_books
            }
        else:
            order_status_response = {
                'status': 'Order Rejected',
                'suggestedBooks': response_books
            }

    logging.info('Order status response created')

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
