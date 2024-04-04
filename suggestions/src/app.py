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


import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# suggestions_pb2_grpc.SuggestionsServiceServicer
class SuggestionsService(suggestions_grpc.SuggestionsServiceServicer):
    # Create an RPC function for book suggestions logic

    myCurrentVC = []

    def startBookSuggestionsMicroService(self, request, context):
        self.myCurrentVC = [0, 0, 0]

        logging.info("Suggestions service started successfully")
        response = suggestions.SuggestionsResponse()
        return response

    def bookSuggestionsEventF(self, request, context):

        response = suggestions.SuggestionsResponse()

        if (self.myCurrentVC == [0, 0, 0]) & (request.newVC == [2, 3, 0]):

            logging.info("Book Suggestions: choosing books (event F)")

            books = self.SuggestionsLogic() # Books as string

            temp = self.myCurrentVC[2]
            self.myCurrentVC = request.newVC # this should become VCc now
            self.myCurrentVC[2] = temp + 1

            logging.info('VC in BooksSuggestions in event F is: ' + str(self.myCurrentVC))

            response.verdict = "Pass"
            response.reason = "ok"
            response.books = books
            return response

            # Here we should return the values to the orchestrator.

        else:
            logging.ERROR("VC ERROR in BookSuggestions in event F!!!")
            response.verdict = "Fail"
            response.reason = "BookSuggestions Verdict: VC error in event F"
            response.books = ""
            return response 
    
    
    def SuggestionsLogic(self):

        # Choices for the suggested books
        books = [
            {'bookId': '123', 'title': 'Dummy Book 1', 'author': 'Author 1'},
            {'bookId': '456', 'title': 'Dummy Book 2', 'author': 'Author 2'},
            {'bookId': '321', 'title': 'Dummy Book 3', 'author': 'Author 3'},
            {'bookId': '654', 'title': 'Dummy Book 4', 'author': 'Author 4'},
            {'bookId': '132', 'title': 'Dummy Book 5', 'author': 'Author 5'},
            {'bookId': '465', 'title': 'Dummy Book 6', 'author': 'Author 6'}
        ]

        # Choosing randomly 2 books
        booksChoice = random.sample(books, 2)

        # Creating the response
        suggestedBooks = booksChoice[0]["bookId"]+ "," + booksChoice[0]["title"]+ "," + booksChoice[0]["author"] + ";" + booksChoice[1]["bookId"]+ "," + booksChoice[1]["title"] + "," + booksChoice[1]["author"]

        logging.info('Suggested books are selected')

        return suggestedBooks
    

    def deleteData(self, request, context):
        self.myCurrentVC = []
    


    

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    suggestions_grpc.add_SuggestionsServiceServicer_to_server(SuggestionsService(), server)

    # Listen on port 50053
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info("Suggestions server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
