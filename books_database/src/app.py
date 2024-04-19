import sys
import os
import grpc
import fileinput
from concurrent import futures
import logging
import random
logging.basicConfig(level=logging.DEBUG)

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/books_database'))
sys.path.insert(0, utils_path)
import books_database_pb2 as books_database
import books_database_pb2_grpc as books_database_grpc


# Create a class to define the server functions, derived from
# books_database_pb2_grpc.DatabaseServiceServicer
class DatabaseService(books_database_grpc.DatabaseServiceServicer):

    def readDatabase(self, request, context):
        title = request.book_title

        response = books_database.DatabaseReadResponse()

        logging.info("Reading the book quantity from database")

        path = os.getcwd() + "/books_database/src/database.txt"
        file = open(path, "r+")
        line = file.readline()
        while line:
            book_info = line.split(",")
            if book_info[0] == title:
                response.quantity = int(book_info[1].strip())
                break
            line = file.readline()
        file.close()

        return response

    def writeDatabase(self, request, context):
        title = request.book_title
        quantity = request.quantity

        logging.info("Writing new book quantity info to database")

        path = os.getcwd() + "/books_database/src/database.txt"
        file = open(path, "r")

        lines = file.readlines()

        for i in range(len(lines)):
            book_info = lines[i].strip().split(",")
            if book_info[0] == title:
                new_quantity = int(book_info[1]) - quantity
                new_line = title + "," + str(new_quantity)
                lines[i] = new_line
            else:
                lines[i] = lines[i].strip()
        
        file.close()

        file = open(path, "w")
        file.write('\n'.join(lines))
        file.close() 

        response = books_database.DatabaseWriteResponse()
        response.verdict = "OK"
        return response
    
    def prepareToExecute(self, request, context):
        
        num = random.random()
        response = books_database.DatabasePrepareResponse()

        if num < 0.1:
            response.verdict = "Fail"
            logging.info("Books Database is not prepared!")
        else:
            response.verdict = "Pass"
            logging.info("Books Database is prepared!")

        return response
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    books_database_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    # Listen on port 50060
    port = "49664"
    server.add_insecure_port("[::]:" + port)

    port = "49665"
    server.add_insecure_port("[::]:" + port)

    port = "49666"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info("Executor server started. Listening on port 49664.")
    logging.info("Executor server started. Listening on port 49665.")
    logging.info("Executor server started. Listening on port 49666.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()