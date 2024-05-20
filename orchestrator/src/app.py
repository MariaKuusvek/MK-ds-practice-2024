import sys
import os
import threading
import logging
import time
import random
logging.basicConfig(level=logging.DEBUG)

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "Service1"
})

traceProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://observability:4318/v1/traces"))
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4318/v1/metrics")
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)
meter = metrics.get_meter("orchestrator.meter")

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

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(2, utils_path)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(2, utils_path)
import order_executor_pb2 as order_executor
import order_executor_pb2_grpc as order_executor_grpc

import grpc

response_verdict = ''
response_reason = ''
response_books = ''

executor_working = 'No'


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
    logging.info("orchestratoris:")
    logging.info(response)
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

def order_queue_func(quantity, title, name, contact, street, city, state, zip, country, ccnr, cvv, expdate, orderId):
    # Establish a connection with the order queue gRPC service.
    with grpc.insecure_channel('order_queue:50054') as channel:
        # Create a stub object.
        stub = order_queue_grpc.QueueServiceStub(channel)
        # Call the service through the stub object.
        response = stub.enqueue(order_queue.QueueRequest(bookQuantity=quantity,
                                                            bookTitle=title,
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
        
def startLeaderElection():

    logging.info("Started leader election.")

    responses = []

    with grpc.insecure_channel('order_executor_1:50056') as channel:
        # Create a stub object.
        stub = order_executor_grpc.ExecutorServiceStub(channel)
        # Call the service through the stub object.
        response_1 = stub.executorAlive(order_executor.ExecutorRequest())
        logging.info("executor 1 heatbeat response: " + str(response_1.verdict))
        responses.append(response_1.verdict)

    with grpc.insecure_channel('order_executor_2:50057') as channel:
        # Create a stub object.
        stub = order_executor_grpc.ExecutorServiceStub(channel)
        # Call the service through the stub object.
        response_2 = stub.executorAlive(order_executor.ExecutorRequest())
        logging.info("executor 2 heatbeat response: " + str(response_2.verdict))
        responses.append(response_2.verdict)

    with grpc.insecure_channel('order_executor_3:50058') as channel:
        # Create a stub object.
        stub = order_executor_grpc.ExecutorServiceStub(channel)
        # Call the service through the stub object.
        response_3 = stub.executorAlive(order_executor.ExecutorRequest())
        logging.info("executor 3 heatbeat response: " + str(response_3.verdict))
        responses.append(response_3.verdict)

    for i in range(3, 0, -1):
        if responses[i-1] == "Yes":

            logging.info("New leader is executor " + str(i))

            while True:
            
                with grpc.insecure_channel('order_executor_'+str(i)+':5005'+str(i+5)) as channel:
                    # Create a stub object.
                    stub = order_executor_grpc.ExecutorServiceStub(channel)
                    # Call the service through the stub object.
                    response = stub.dequeueOrder(order_executor.ExecutorRequest())

                checkLeaderHeartBeat(i)
                

def checkLeaderHeartBeat(leaderId):

    with grpc.insecure_channel('order_executor_'+str(leaderId)+':5005'+str(leaderId+5)) as channel:
        # Create a stub object.
        stub = order_executor_grpc.ExecutorServiceStub(channel)
        # Call the service through the stub object.
        response = stub.executorAlive(order_executor.ExecutorRequest())
    
    if response.verdict == "Yes":
        logging.info("Executor " + str(leaderId) + " is the leader.")
        time.sleep(15)
    else:
        startLeaderElection()


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

firstTimeOnAHomePage = 0

# Define a GET endpoint.
@app.route('/')
def index():
    pass
    
    #if firstTimeOnAHomePage == 0:
    #    # Start leader election
    #    startLeaderElection()
    #    firstTimeOnAHomePage = 1


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """

    logging.info('Checkout REST started')

    # Verification failed counter
    ver_fail_counter = meter.create_counter(name="verification_fails", description="number of verifications that failed", value_type=int)


    #startLeaderElection()
   
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
                                                                                        str(orderId)))
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

#
    # Creating response based on the results of the microservices
    if response_verdict != '' and response_reason != '':
        if response_verdict == 'Pass':

            # Putting the verified order into a queue
            order_queue_func(request.json['items'][0]['quantity'],
                                request.json['items'][0]['name'],
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
                                str(orderId))
            

            global executor_working
            # Choosing an executor and executing the order
            while True :
                if executor_working == 'Yes':
                    time.sleep(1)
                else: 
                    executor_working = "Yes"
                    # Choosing an executer
                    index = random.choice(range(1, 4))

                    logging.info("order_executor"+str(index)+':5005'+str(index+5)+" has the right to access data.")

                    # Executing an order
                    with grpc.insecure_channel('order_executor_'+str(index)+':5005'+str(index+5)) as channel:
                        stub = order_executor_grpc.ExecutorServiceStub(channel)
                        response_executor = stub.dequeueOrder(order_executor.ExecutorRequest())
                    executor_working = "No"
                    break

            books = response_books.split(";")
            books_object = []
            for i in range(len(books)):
                book_info = books[i].split(",")
                books_object.append({'bookId': book_info[0], 'title': book_info[1], 'author': book_info[2]})

            if response_executor.verdict == "Fail":
                order_status_response = {
                'orderId': orderId,
                'status': 'Order Rejected',
                'suggestedBooks': []
                }  
            else:
                order_status_response = {
                    'orderId': orderId,
                    'status': 'Order Approved',
                    'suggestedBooks': books_object
                }
        else:

            ver_fail_counter.add(1, {"fail_type": "ver_fail", "handled_by_user": True})

            order_status_response = {
                'orderId': orderId,
                'status': 'Order Rejected',
                'suggestedBooks': []
            }


    logging.info('Order status response created')

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
