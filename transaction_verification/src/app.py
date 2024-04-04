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

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(2, utils_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc


# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.VerificationServiceServicer
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    
    myCurrentVC = []
    itemsLength = 0
    userName = ''
    userContact = ''
    street = ''
    city = ''
    state = ''
    zip = ''
    country = ''
    creditcardnr = ''
    cvv = ''
    expirationDate = ''

    def startTransVerMicroService(self, request, context):

        response = transaction_verification.VerificationResponse()

        self.myCurrentVC = [0, 0, 0]
        self.itemsLength = request.itemsLength
        self.userName = request.userName
        self.userContact = request.userContact
        self.street = request.street
        self.city = request.city
        self.state = request.state
        self.zip = request.zip
        self.country = request.country
        self.creditcardnr = request.creditcardnr
        self.cvv = request.cvv
        self.expirationDate = request.expirationDate

        logging.info("Transaction Service started successfully")

        request = transaction_verification.VerificationRequest(orderId = request.orderId, newVC = [0, 0, 0])

        response = self.itemsLengthEventA(request)

        logging.info(response)
        return response

    
    def itemsLengthEventA(self, request):

        response = transaction_verification.VerificationResponse()

        if self.myCurrentVC == [0, 0, 0]:

            logging.info("Transaction verification: checking items length (event A)")
            # If all contitions are True, then the verification passed.
            if self.itemsLength != 0:
                logging.info("Transaction verification verdict: Pass")
                verdict = "Pass"
            else:
                logging.info("Transaction verification verdict: Fail")
                verdict = "Fail"

            if verdict == "Fail":

                # Deleting data in microservices
                request = transaction_verification.VerificationDeleteRequest()
                self.deleteDataInMicroservices(request)

                # Return fail response
                response.verdict = "Fail"
                response.reason = "TransVer Verdict: no items in the cart"
                response.books = ""
                return response

            self.myCurrentVC[1] = self.myCurrentVC[1] + 1 # this should become VCc now
            logging.info('VC in TransVer in event A is: ' + str(self.myCurrentVC))

            request = transaction_verification.VerificationRequest(orderId = request.orderId, newVC = self.myCurrentVC)
            return self.userDataEventB(request) # sync, async, whatever we want

        else:

            # Deleting data in microservices
            request = transaction_verification.VerificationDeleteRequest()
            self.deleteDataInMicroservices(request)

            logging.ERROR("VC ERROR in TransVer in event A!!!")
            response.verdict = "Fail"
            response.reason = "TransVer Verdict: VC error in event A"
            response.books = ""
            return response 


    def userDataEventB(self, request):

        response = transaction_verification.VerificationResponse()

        if (self.myCurrentVC == [0, 1, 0]) & (list(request.newVC) == [0, 1, 0]):

            logging.info("Transaction verification: checking user data (event B)")
            # Event logic
            checkUserInfo = self.userName != "" and self.userContact != ""
            checkBillingAddress = self.street != "" and self.city != "" and self.state != "" and self.zip != "" and self.country != "" 
            # If all contitions are True, then the verification passed.
            if all([checkUserInfo, checkBillingAddress]):
                logging.info("Transaction verification verdict: Pass")
                verdict = "Pass"
            else:
                logging.info("Transaction verification verdict: Fail")
                verdict = "Fail"

            if verdict == "Fail":

                # Deleting data in microservices
                request = transaction_verification.VerificationDeleteRequest()
                self.deleteDataInMicroservices(request)

                response.verdict = "Fail"
                response.reason = "TransVer Verdict: incorrect user data"
                response.books = ""
                return response
        
            temp = self.myCurrentVC[1]
            self.myCurrentVC = request.newVC # this should become VCc now
            self.myCurrentVC[1] = temp + 1
            logging.info('VC in TransVer in event B is: ' + str(self.myCurrentVC))

            channel = grpc.insecure_channel('fraud_detection:50051')
            stub = fraud_detection_grpc.FraudServiceStub(channel)
            request = fraud_detection.FraudRequest(orderId = request.orderId, newVC = self.myCurrentVC)
            response = stub.userDataEventC(request)

            return response
        
        else:

            # Deleting data in microservices
            request = transaction_verification.VerificationDeleteRequest()
            self.deleteDataInMicroservices(request)

            logging.ERROR("VC ERROR in TransVer in event B!!!")
            response.verdict = "Fail"
            response.reason = "TransVer Verdict: VC error in event B"
            response.books = ""
            return response 
    
    def creditCardEventD(self, request, context):

        response = transaction_verification.VerificationResponse()

        if (self.myCurrentVC == [0, 2, 0]) & (request.newVC == [1, 2, 0]):

            logging.info("Transaction verification: checking credit card (event D)")

            checkCreditCardNr = len(self.creditcardnr) >= 10
            checkCVVnr = len(self.cvv) == 3 or len(self.cvv) == 4
            ab = re.compile("\d\d\/\d\d")
            checkExpirationDate = ab.match(self.expirationDate) and int(self.expirationDate[:2]) <= 12 and int(self.expirationDate[3:]) > 23

            # If all contitions are True, then the verification passed.
            if all([checkCreditCardNr, checkCVVnr, checkExpirationDate]):
                logging.info("Transaction verification verdict: Pass")
                verdict = "Pass"
            else:
                logging.info("Transaction verification verdict: Fail")
                verdict = "Fail"

            if verdict == "Fail":

                # Deleting data in microservices
                request = transaction_verification.VerificationDeleteRequest()
                self.deleteDataInMicroservices(request)

                response.verdict = "Fail"
                response.reason = "TransVer Verdict: incorrect credit card"
                response.books = ""
                return response
        
            temp = self.myCurrentVC[1]
            self.myCurrentVC = request.newVC # this should become VCc now
            self.myCurrentVC[1] = temp + 1

            logging.info('VC in TransVer in event D is: ' + str(self.myCurrentVC))

            channel = grpc.insecure_channel('fraud_detection:50051')
            stub = fraud_detection_grpc.FraudServiceStub(channel)
            request = fraud_detection.FraudRequest(orderId = request.orderId, newVC = self.myCurrentVC)
            response = stub.creditCardEventE(request)

            return response

        else:

            # Deleting data in microservices
            request = transaction_verification.VerificationDeleteRequest()
            self.deleteDataInMicroservices(request)

            logging.ERROR("VC ERROR in TransVer in event D!!!")
            response.verdict = "Fail"
            response.reason = "TransVer Verdict: VC error in event D"
            response.books = ""
            return response 
        

    def deleteDataInMicroservices(self, request, context):
        channel = grpc.insecure_channel('fraud_detection:50051')
        stub = fraud_detection_grpc.FraudServiceStub(channel)
        request = fraud_detection.FraudDeleteRequest()
        response = stub.deleteData(request)

        channel = grpc.insecure_channel('suggestions:50053')
        stub = suggestions_grpc.FraudServiceStub(channel)
        request = suggestions.SuggestionsDeleteRequest()
        response = stub.deleteData(request)

        request = transaction_verification.VerificationDeleteRequest()
        self.deleteData(request)


    def deleteData(self, request, context):

        self.myCurrentVC = []
        self.itemsLength = 0
        self.userName = ''
        self.userContact = ''
        self.street = ''
        self.city = ''
        self.state = ''
        self.zip = ''
        self.country = ''
        self.creditcardnr = ''
        self.cvv = ''
        self.expirationDate = ''


    
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
