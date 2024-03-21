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

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc


# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.VerificationServiceServicer
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    # Create an RPC function for transaction verification logic
    def VerificationLogic(self, request, context):
        # Create a VerificationResponse object
        response = transaction_verification.VerificationResponse()
        
        # Greeting message
        logging.info("Hello from the Transaction Verification microservice")

        # Defining conditions for the verification process
        checkItemsLength = request.itemsLength != 0
        checkUserInfo = request.userName != "" and request.userContact != ""
        checkBillingAddress = request.street != "" and request.city != "" and request.state != "" and request.zip != "" and request.country != "" 
        checkCreditCardNr = len(request.creditcardnr) >= 10
        checkCVVnr = len(request.cvv) == 3 or len(request.cvv) == 4
        ab = re.compile("\d\d\/\d\d")
        checkExpirationDate = ab.match(request.expirationDate) and int(request.expirationDate[:2]) <= 12 and int(request.expirationDate[3:]) > 23

        # If all contitions are True, then the verification passed.
        if all([checkItemsLength, checkUserInfo, checkBillingAddress, checkCreditCardNr, checkCVVnr, checkExpirationDate]):
            logging.info("Transaction verification verdict: Pass")
            response.verdict = "Pass"
            return response
        else:
            logging.info("Transaction verification verdict: Pass")
            response.verdict = "Fail"
            return response
        
    def VerificationMakeRequestFraud(self):
        channel = grpc.insecure_channel('localhost:50051')
        stub = fraud_detection_grpc.FraudServiceStub(channel)
        request = fraud_detection.FraudVCIndex(value = 0)
        response = stub.FraudRespondRequest(request)
        return response

    def VerificationRespondRequest(self, index):
        clock = [6, 7, 8]
        return clock[index]
        
       
    
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
