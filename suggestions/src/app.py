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

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# suggestions_pb2_grpc.SuggestionsServiceServicer
class SuggestionsService(suggestions_grpc.SuggestionsServiceServicer):
    # Create an RPC function for book suggestions logic
    def SuggestionsLogic(self, request, context):
        # Create a SuggestionsResponse object
        response = suggestions.SuggestionsResponse()

        # Greeting message
        logging.info('Hello from the Book Suggestions microservice')

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
        response.book1id = booksChoice[0]["bookId"]
        response.book1name = booksChoice[0]["title"]
        response.book1author = booksChoice[0]["author"]
        response.book2id = booksChoice[1]["bookId"]
        response.book2name = booksChoice[1]["title"]
        response.book2author = booksChoice[1]["author"]

        logging.info('Suggested books are selected')

        return response

    

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
    print("Server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
