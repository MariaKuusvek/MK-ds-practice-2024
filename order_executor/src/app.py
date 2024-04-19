import sys
import os
import random
import logging
import time
logging.basicConfig(level=logging.DEBUG)

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(1, utils_path)
import order_executor_pb2 as order_executor
import order_executor_pb2_grpc as order_executor_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(2, utils_path)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/books_database'))
sys.path.insert(2, utils_path)
import books_database_pb2 as books_database
import books_database_pb2_grpc as books_database_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment_system'))
sys.path.insert(2, utils_path)
import payment_system_pb2 as payment_system
import payment_system_pb2_grpc as payment_system_grpc


import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# order_queue_pb2_grpc.QueueServiceServicer
class ExecutorService(order_executor_grpc.ExecutorServiceServicer):
    # Create an RPC function for queue logic

    iAmAlive = 1

    def dequeueOrder(self, request, context):

        logging.info("Dequeuing started in executor")
        response = order_executor.ExecutorResponse()

        channel = grpc.insecure_channel('order_queue:50054')
        stub = order_queue_grpc.QueueServiceStub(channel)
        request = order_queue.QueueRequest()
        responseQueue = stub.queueHasElements(request)

        if responseQueue.verdict == "Yes":
            channel = grpc.insecure_channel('order_queue:50054')
            stub = order_queue_grpc.QueueServiceStub(channel)
            request = order_queue.QueueRequest()
            responseQueue = stub.dequeue(request)
            
            logging.info("Order is being executed…")

            # Read from database
            channel = grpc.insecure_channel('books_database_1:49664')
            stub = books_database_grpc.DatabaseServiceStub(channel)
            request = books_database.DatabaseReadRequest(book_title=responseQueue.bookTitle)
            responseDatabase = stub.readDatabase(request)

            if responseDatabase.quantity <= 0:
                response.verdict = "Fail"
                return response


            prepareResponse = self.askForServicePrepared()

            if prepareResponse == "Pass" :
                commitResponse = self.commitChanges(responseQueue.bookTitle, responseQueue.bookQuantity)
                if commitResponse != "Pass":
                    response.verdict = "Fail"
                    return response
            else :
                response.verdict = "Fail"
                return response
                        
            self.iAmAlive = 0
            response.verdict = "Pass"
            return response

        else:
            logging.info("No order to execute")
            response.verdict = "No order"
            return response

    
    def executorAlive(self, request, context):
        response = order_executor.ExecutorResponse()
        if self.iAmAlive == 1:
            response.verdict = "Yes"
        else:
            response.verdict = "No"
        return response
    

    def askForServicePrepared(self):

        channel = grpc.insecure_channel('books_database_1:49664')
        stub = books_database_grpc.DatabaseServiceStub(channel)
        request = books_database.DatabasePrepareRequest()
        responseDatabase = stub.prepareToExecute(request)

        channel = grpc.insecure_channel('payment_system:49667')
        stub = payment_system_grpc.PaymentServiceStub(channel)
        request = payment_system.PaymentRequest()
        responsePayment = stub.prepareToExecute(request)

        if responseDatabase.verdict == "Pass" and responsePayment.verdict == "Pass":
            return "Pass"
        else:
            return "Fail"
        
    def commitChanges(self, bookTitle, bookQuantity):

        # Write to database
        channel = grpc.insecure_channel('books_database_1:49664')
        stub = books_database_grpc.DatabaseServiceStub(channel)
        request = books_database.DatabaseWriteRequest(book_title=bookTitle, quantity=bookQuantity)
        responseDatabase = stub.writeDatabase(request)

        channel = grpc.insecure_channel('payment_system:49667')
        stub = payment_system_grpc.PaymentServiceStub(channel)
        request = payment_system.PaymentRequest()
        responsePayment = stub.paymentLogic(request)

        if responseDatabase.verdict == "OK" and responsePayment.verdict == "OK":
            return "Pass"
        else:
            return "Fail"





def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_executor_grpc.add_ExecutorServiceServicer_to_server(ExecutorService(), server)

    # Listen on port 50055
    port = "50056"
    server.add_insecure_port("[::]:" + port)

    port = "50057"
    server.add_insecure_port("[::]:" + port)

    port = "50058"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info("Executor server started. Listening on port 50056.")
    logging.info("Executor server started. Listening on port 50057.")
    logging.info("Executor server started. Listening on port 50058.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
