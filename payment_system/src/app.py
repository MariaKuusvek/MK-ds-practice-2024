import sys
import os
import grpc
from concurrent import futures
import logging
import random
logging.basicConfig(level=logging.DEBUG)

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment_system'))
sys.path.insert(0, utils_path)
import payment_system_pb2 as payment_system
import payment_system_pb2_grpc as payment_system_grpc


# Create a class to define the server functions, derived from
# payment_system_pb2_grpc.PaymentServiceServicer
class PaymentService(payment_system_grpc.PaymentServiceServicer):

    def paymentLogic(self, request, context):
        response = payment_system.PaymentResponse()
        response.verdict = "OK"
        logging.info("Payment Logic Executed!")
        return response
    
    def prepareToExecute(self, request, context):
        num = random.random()
        response = payment_system.PaymentResponse()

        if num < 0.1:
            response.verdict = "Fail"
            logging.info("Payment System is not prepared!")
        else:
            response.verdict = "Pass"
            logging.info("Payment System is prepared!")

        return response
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    payment_system_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)

    # Listen on port 49667
    port = "49667"
    server.add_insecure_port("[::]:" + port)

    # Start the server
    server.start()
    logging.info("Executor server started. Listening on port 49667.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()