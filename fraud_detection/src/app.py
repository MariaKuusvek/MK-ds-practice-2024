import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.FraudServiceServicer
class FraudService(fraud_detection_grpc.FraudServiceServicer):
    # Create an RPC function for fraud detection logic
    def FraudLogic(self, request, context):
        # Create a FraudResponse object
        response = fraud_detection.FraudResponse()

        # Greeting message
        print("Hello from the Fraud Detection microservice")

        card = request.creditcardnr
        
        # Checking that the credit card number is not made up only one number.
        for i in range(1, len(card)):
            if card[i] == card[0]:
                response.verdict = "Fraud"
            else: 
                response.verdict = "Not Fraud"
                break
        
        print("Fraud Logic verdict: " + response.verdict)
        return response

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
    print("Server started. Listening on port 50051.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()