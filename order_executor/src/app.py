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
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, utils_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(1, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(1, utils_path)
import order_executor_pb2 as order_executor
import order_executor_pb2_grpc as order_executor_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(2, utils_path)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc


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
        stub = order_queue.QueueServiceStub(channel)
        request = order_queue_grpc.QueueRequest()
        response = stub.queueHasElements(request)

        if response.verdict == "Yes":
            channel = grpc.insecure_channel('order_queue:50054')
            stub = order_queue.QueueServiceStub(channel)
            request = order_queue_grpc.QueueRequest()
            response = stub.dequeue(request)
            
            logging.info("Order is being executed…")
            response.verdict = "Order executed"
            self.iAmAlive = 0
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
