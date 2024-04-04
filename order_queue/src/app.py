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

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(1, utils_path)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc


import grpc
from concurrent import futures
from collections import deque
import math
#import osmnx as ox

# Create a class to define the server functions, derived from
# order_queue_pb2_grpc.QueueServiceServicer
class QueueService(order_queue_grpc.QueueServiceServicer):
    queue = []

    # Create an RPC function for queue logic

    def enqueue(self, request, context):
        logging.info("Enqueue started")

        # We build the queue priority based on the distance between the users city and Tartu
        #area1 = ox.geocode_to_gdf(request.city).geometry.centroid
        #area2 = ox.geocode_to_gdf("Tartu").geometry.centroid#

        #distance = math.sqrt((area2.x - area1.x)**2 + (area2.y - area1.y)**2)

        order = {
            "orderId": request.orderId,
            "orderInfo": {
                "itemsLength": request.itemsLength,
                "userName": request.userName,
                "userContact": request.userContact,
                "street": request.street,
                "city": request.city,
                "state": request.state,
                "zip": request.zip,
                "country": request.country,
                "creditcardnr": request.creditcardnr,
                "cvv": request.cvv,
                "expirationDate": request.expirationDate,
            },
            #"distance": distance
        }
        #logging.info("Distance: " + str(distance))

        #for previousOrder in self.queue:
        #     if previousOrder["distance"] > distance:
        #          inx = self.queue.index(previousOrder)
        #          self.queue.insert(inx, order)

        self.queue.append(order)

        logging.info("Order ID " +  request.orderId + " entered into queue")
        logging.info(self.queue)

        response = order_queue.QueueResponse()
        response.verdict = "Pass"

        return response

    def dequeue(self, request, context):
        logging.info("Dequeue started")

        currentOrder = self.queue[0]
        del self.queue[0]
        logging.info ("Order ID "  + currentOrder["orderId"] + " removed from queue")
        

        response = order_queue.QueueResponseDequeue()

        response.itemsLength = currentOrder["orderInfo"]["itemsLength"]
        response.userName = currentOrder["orderInfo"]["userName"]
        response.street = currentOrder["orderInfo"]["street"]
        response.city = currentOrder["orderInfo"]["city"]
        response.state = currentOrder["orderInfo"]["state"]
        response.zip = currentOrder["orderInfo"]["zip"]
        response.country = currentOrder["orderInfo"]["country"]
        response.creditcardnr = currentOrder["orderInfo"]["creditcardnr"]
        response.cvv = currentOrder["orderInfo"]["cvv"]
        response.expirationDate = currentOrder["orderInfo"]["expirationDate"]
        response.orderId = currentOrder["orderId"]

        return response
    
    def queueHasElements(self, request, context):
        response = order_queue.QueueResponse()

        if not bool(self.queue):
            response.verdict = "No"
            return response
        else:
            response.verdict = "Yes"
            return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_queue_grpc.add_QueueServiceServicer_to_server(QueueService(), server)

    # Listen on port 50054
    port = "50054"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    logging.info("Queue server started. Listening on port 50054.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
