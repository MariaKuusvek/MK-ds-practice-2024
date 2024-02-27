
import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures
import re

# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.HelloServiceServicer
class HelloService(transaction_verification_grpc.HelloServiceServicer):
    # Create an RPC function to say hello
    def SayHello(self, request, context):
        # Create a HelloResponse object
        response = transaction_verification.HelloResponse()
        # Set the greeting field of the response object
        response.greeting = "Hello, " + request.name
        # Print the greeting message
        print(response.greeting)
        # Return the response object
        return response
    
    def verification_logic(info):
        
        if len(info["items"]) == 0:
            return "Fail"
        
        if info["user"]["name"] == "" or info["user"]["contact"] == "":
            return "Fail"
        
        if info["billingAddress"]["street"] == "" or info["billingAddress"]["city"] == "" or info["billingAddress"]["state"] == "" or info["billingAddress"]["zip"] == "" or info["billingAddress"]["country"] == "" :
            return "Fail"
        
        if len(info["creditCard"]["number"]) != 10:
            return "Fail"
        
        if len(info["creditCard"]["cvv"]) != 3 or len(info["creditCard"]["cvv"]) != 4:
            return "Fail"
        
        ab = re.compile("\d\d\/\d\d")
        if ab.match(info["creditCard"]["expirationDate"]) and info["creditCard"]["expirationDate"][:2] <= 12 and info["creditCard"]["expirationDate"][3:] > 23:
            return "Pass"
        else:
            return "Fail"
        
        return "verified logic"

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    transaction_verification_grpc.add_HelloServiceServicer_to_server(HelloService(), server)

    # Listen on port 50052
    port = "50052"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
