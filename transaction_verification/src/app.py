import sys
import os
import grpc
from concurrent import futures
import re
import logging
logging.basicConfig(level=logging.DEBUG)

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc


# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.VerificationServiceServicer
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    # Create an RPC function for transaction verification logic
    def VerificationLogic(self, request, context):
        # Create a VerificationResponse object
        response = transaction_verification.VerificationResponse()
        
        # Greeting message
        logging.info("Hello from the Transaction Verification microservice")
  
        # Checking the nr of books
        if request.itemsLength == 0:
            response.verdict = "Fail"
            return response

        # Checking user info
        if request.userName == "" or request.userContact == "":
            response.verdict = "Fail"
            return response
        
        # Checking billing address info
        if request.street == "" or request.city == "" or request.state == "" or request.zip == "" or request.country == "" :
            response.verdict = "Fail"
            return response

        # Checking credit card nr:
        if len(request.creditcardnr) < 10:
            response.verdict = "Fail"
            return response

        # Checking CVV nr:
        if len(request.cvv) != 3 and len(request.cvv) != 4:
            response.verdict = "Fail"
            return response
        
        # Checking the expiration date:
        ab = re.compile("\d\d\/\d\d")
        if ab.match(request.expirationDate) and int(request.expirationDate[:2]) <= 12 and int(request.expirationDate[3:]) > 23:
            response.verdict = "Pass"
            return response
        else:
            response.verdict = "Fail"
            return response
        
       
    
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
    logging.info("Transaction Verifiction server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
