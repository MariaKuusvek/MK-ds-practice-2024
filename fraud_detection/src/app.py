import sys
import os
import logging
logging.basicConfig(level=logging.DEBUG)

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

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.FraudServiceServicer
class FraudService(fraud_detection_grpc.FraudServiceServicer):

    myCurrentVC = []
    creditCardNr = ''
    userName = ''
    userContact = ''

    def startFraudDecMicroService(self, request, context):
        self.myCurrentVC = [0, 0, 0]
        self.creditCardNr = request.creditCardNr
        self.userName = request.userName
        self.userContact = request.userContact

        logging.info("Fraud Detection started successfully")
        response = fraud_detection.FraudResponse()
        return response

    def userDataEventC(self, request, context):

        response = fraud_detection.FraudResponse()

        if (self.myCurrentVC == [0, 0, 0]) & (request.newVC == [0, 2, 0]):

            logging.info("Fraud Detection: checking user data (event C)")

            verdict = self.FraudCheckUserData() 

            if verdict == 'Fail':

                # Deleting data in microservices
                request = fraud_detection.FraudDeleteRequest()
                self.deleteDataInMicroservices(request)

                response.verdict = "Fail"
                response.reason = "FraudDetection Verdict: incorrect user data"
                response.books = ""
                return response
            
            temp = self.myCurrentVC[0]
            self.myCurrentVC = request.newVC # this should become VCc now
            self.myCurrentVC[0] = temp + 1

            logging.info('VC in FraudService in event C is: ' + str(self.myCurrentVC))

            channel = grpc.insecure_channel('transaction_verification:50052')
            stub = transaction_verification_grpc.VerificationServiceStub(channel)
            request = transaction_verification.VerificationRequest(orderId = request.orderId, newVC = self.myCurrentVC)
            response = stub.creditCardEventD(request)
            return response

        else:

            # Deleting data in microservices
            request = fraud_detection.FraudDeleteRequest()
            self.deleteDataInMicroservices(request)

            logging.ERROR("VC ERROR in FraudService in event C!!!")
            response.verdict = "Fail"
            response.reason = "FraudDetection Verdict: VC error in event C"
            response.books = ""
            return response 

    def creditCardEventE(self, request, context):
        response = fraud_detection.FraudResponse()

        if (self.myCurrentVC == [1, 2, 0]) & (request.newVC == [1, 3, 0]):

            logging.info("Fraud Detection: checking credit card (event E)")

            verdict = self.FraudCheckCreditCard()

            if verdict == 'Fail':

                # Deleting data in microservices
                request = fraud_detection.FraudDeleteRequest()
                self.deleteDataInMicroservices(request)

                response.verdict = "Fail"
                response.reason = "FraudDetection Verdict: incorrect credit card"
                response.books = ""
                return response
            
            temp = self.myCurrentVC[0]
            self.myCurrentVC = request.newVC # this should become VCc now
            self.myCurrentVC[0] = temp + 1

            logging.info('VC in FraudService in event E is: ' + str(self.myCurrentVC))

            channel = grpc.insecure_channel('suggestions:50053')
            stub = suggestions_grpc.SuggestionsServiceStub(channel)
            request = suggestions.SuggestionsRequest(orderId = request.orderId, newVC = self.myCurrentVC)
            response = stub.bookSuggestionsEventF(request)
            return response

        else:

            # Deleting data in microservices
            request = fraud_detection.FraudDeleteRequest()
            self.deleteDataInMicroservices(request)

            logging.ERROR("VC ERROR in FraudService in event E!!!")
            response.verdict = "Fail"
            response.books = ""
            return response 
        
 
    def FraudCheckUserData(self):

        logging.info('Fraud Detection: checking User Data')
        
        indexName = self.userName.find(' ')
        # Cheking that the name has space in it.
        if indexName != -1:
            # Checking that the user contact has the character '@'.
            indexContaxt = self.userContact.find('@')
            if indexContaxt != -1:
                verdict = "Pass"
            else:
                verdict = "Fail"
        else:
            verdict = "Fail"

        logging.info("Fraud Logic verdict: " + verdict)
        return verdict


    def FraudCheckCreditCard(self):

        logging.info('Fraud Detection: checking credit card')

        # Checking that the credit card number is not made up only one number.
        for i in range(1, len(self.creditCardNr)):
            if self.creditCardNr[i] == self.creditCardNr[0]:
                verdict = "Fail"
            else: 
                verdict = "Pass"
                break
        
        logging.info("Fraud Logic verdict: " + verdict)
        return verdict
    
    
    def deleteDataInMicroservices(self, request):
        channel = grpc.insecure_channel('transaction_verification:50052')
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        request = transaction_verification.VerificationDeleteRequest()
        response = stub.deleteData(request)

        channel = grpc.insecure_channel('suggestions:50053')
        stub = suggestions_grpc.SuggestionsServiceStub(channel)
        request = suggestions.SuggestionsDeleteRequest()
        response = stub.deleteData(request)

        self.myCurrentVC = []
        self.creditCardNr = ''
        self.userName = ''
        self.userContact = ''

        logging.info("Data deleted from microservices")
    
    def deleteData(self, request, context):

        self.myCurrentVC = []
        self.creditCardNr = ''
        self.userName = ''
        self.userContact = ''
        return fraud_detection.FraudDeleteResponse()



    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    fraud_detection_grpc.add_FraudServiceServicer_to_server(FraudService(), server)
    # Listen on port 50051
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info("Fraud Detection server started. Listening on port 50051.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()