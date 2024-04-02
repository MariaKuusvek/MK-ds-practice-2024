import sys
import os
import random
import logging
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


import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# order_queue_pb2_grpc.QueueServiceServicer
class ExecutorService(order_executor_grpc.ExecutorServiceServicer):
    # Create an RPC function for queue logic

    def func1(self, request, context):
        logging.info("func1 started successfully")

        response = order_executor.ExecutorResponse()
        return response

    def func2(self, request, context):
        logging.info("func2 started successfully")

        response = order_executor.ExecutorResponse()
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_executor_grpc.add_ExecutorServiceServicer_to_server(ExecutorService(), server)

    # Listen on port 50055
    port = "50056"
    server.add_insecure_port("[::]:" + port)

    #port = "50057"
    #server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info("Executor server started. Listening on port 50056.")
    #logging.info("Executor server started. Listening on port 50057.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
