
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
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    # Create an RPC function to say hello
    def VerificationLogic(self, request, context):
        # Create a HelloResponse object
        response = transaction_verification.VerificationResponse()
        
        # Greeting message
        print("Hello from the Transaction Verification microservice")
  
        if request.itemsLength == 0:
            return "Fail"
        
        if request.userName == "" or request.userContact == "":
            return "Fail"
        
        if request.street == "" or request.city == "" or request.state == "" or request.zip == "" or request.country == "" :
            return "Fail"
        
        if len(request.creditcardnr) <= 10:
            return "Fail"
        
        if len(request.cvv) != 3 or len(request.cvv) != 4:
            return "Fail"
        
        print("HEEEEIIIII")
        
        ab = re.compile("\d\d\/\d\d")
        if ab.match(request.expirationDate) and request.expirationDate[:2] <= 12 and request.expirationDate[3:] > 23:
           return "Pass"
        else:
            return "Fail"
        
       
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    transaction_verification_grpc.add_VerificationServiceServicer_to_server(VerificationService(), server)

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
