from locust import HttpUser, task
import logging
from json import JSONDecodeError
import os

class TestingUser(HttpUser):
    #wait_time = between(1, 5)

    @task(7)
    def successReponseBook1(self):
        logging.info("Beginning Success Case Book 1")
        with self.client.post("http://localhost:8081/checkout", json={'user': {'name': 'near near ', 'contact': 'MK@MK.com'}, 'creditCard': {'number': '1234567890', 'expirationDate': '12/52', 'cvv': '123'}, 'userComment': '', 'items': [{'name': 'Learning Python', 'quantity': 1}], 'discountCode': '', 'shippingMethod': '', 'giftMessage': '', 'billingAddress': {'street': 'Ranna Tee 1', 'city': 'Tartu', 'state': 'County', 'zip': '51008', 'country': 'Estonia'}, 'giftWrapping': False, 'termsAndConditionsAccepted': True, 'notificationPreferences': ['email'], 'device': {'type': 'Smartphone', 'model': 'Samsung Galaxy S10', 'os': 'Android 10.0.0'}, 'browser': {'name': 'Chrome', 'version': '85.0.4183.127'}, 'appVersion': '3.0.0', 'screenResolution': '1440x3040', 'referrer': 'https://www.google.com', 'deviceLanguage': 'en-US'}, catch_response=True) as response:

            # Checking that database value went down
            path = os.getcwd() + "/books_database/src/database.txt"
            file = open(path, "r")
            lines = file.readlines()
            for i in range(len(lines)):
                book_info = lines[i].strip().split(",")
                if book_info[0] == "Learning Python":
                    quantity = book_info[1]
                    break
            file.close()

            try:
                logging.info(response.json())
                if not (response.json()["status"] == "Order Approved" or (response.json()["status"] == "Order Rejected" and quantity == "0")):
                    logging.info("Did not get expected value in status")
                    response.failure("Did not get expected value in status")
                else:
                    logging.info("Correct reponse to successful order")
                    response.success()
            except JSONDecodeError:
                logging.info("Could not be decoded as JSON")
                response.failure("Response could not be decoded as JSON")
            except KeyError:
                response.failure("Response did not contain expected key 'greeting'")

    @task(7)
    def successReponseBook2(self):
        logging.info("Beginning Success Case Book 2")
        with self.client.post("http://localhost:8081/checkout", json={'user': {'name': 'near near ', 'contact': 'MK@MK.com'}, 'creditCard': {'number': '1234567890', 'expirationDate': '12/52', 'cvv': '123'}, 'userComment': '', 'items': [{'name': 'Domain-Driven Design: Tackling Complexity in the Heart of Software', 'quantity': 1}], 'discountCode': '', 'shippingMethod': '', 'giftMessage': '', 'billingAddress': {'street': 'Ranna Tee 1', 'city': 'Tartu', 'state': 'County', 'zip': '51008', 'country': 'Estonia'}, 'giftWrapping': False, 'termsAndConditionsAccepted': True, 'notificationPreferences': ['email'], 'device': {'type': 'Smartphone', 'model': 'Samsung Galaxy S10', 'os': 'Android 10.0.0'}, 'browser': {'name': 'Chrome', 'version': '85.0.4183.127'}, 'appVersion': '3.0.0', 'screenResolution': '1440x3040', 'referrer': 'https://www.google.com', 'deviceLanguage': 'en-US'}, catch_response=True) as response:

            # Checking that database value went down
            path = os.getcwd() + "/books_database/src/database.txt"
            file = open(path, "r")
            lines = file.readlines()
            for i in range(len(lines)):
                book_info = lines[i].strip().split(",")
                if book_info[0] == "Learning Python":
                    quantity = book_info[1]
                    break
            file.close()

            try:
                logging.info(response.json())
                if not (response.json()["status"] == "Order Approved" or (response.json()["status"] == "Order Rejected" and quantity == "0")):
                    logging.info("Did not get expected value in status")
                    response.failure("Did not get expected value in status")
                else:
                    logging.info("Correct reponse to successful order")
                    response.success()
            except JSONDecodeError:
                logging.info("Could not be decoded as JSON")
                response.failure("Response could not be decoded as JSON")
            except KeyError:
                response.failure("Response did not contain expected key 'greeting'")


    @task
    def failReponseName(self):
        logging.info("Beginning Fail Case: No space in name")
        with self.client.post("http://localhost:8081/checkout", json={'user': {'name': 'nospace', 'contact': 'MK@MK.com'}, 'creditCard': {'number': '1234567890', 'expirationDate': '12/52', 'cvv': '123'}, 'userComment': '', 'items': [{'name': 'Learning Python', 'quantity': 1}], 'discountCode': '', 'shippingMethod': '', 'giftMessage': '', 'billingAddress': {'street': 'Ranna Tee 1', 'city': 'Tartu', 'state': 'County', 'zip': '51008', 'country': 'Estonia'}, 'giftWrapping': False, 'termsAndConditionsAccepted': True, 'notificationPreferences': ['email'], 'device': {'type': 'Smartphone', 'model': 'Samsung Galaxy S10', 'os': 'Android 10.0.0'}, 'browser': {'name': 'Chrome', 'version': '85.0.4183.127'}, 'appVersion': '3.0.0', 'screenResolution': '1440x3040', 'referrer': 'https://www.google.com', 'deviceLanguage': 'en-US'}, catch_response=True) as response:
            try:
                logging.info(response.json())
                if response.json()["status"] != "Order Rejected":
                    logging.info("Did not get expected value in status")
                    response.failure("Did not get expected value in status")
                else:
                    logging.info("Correct response to unsuccessful order")
                    response.success()
            except JSONDecodeError:
                logging.info("Could not be decoded as JSON")
                response.failure("Response could not be decoded as JSON")
            except KeyError:
                response.failure("Response did not contain expected key 'greeting'")

    @task
    def failReponseCreditCard(self):
        logging.info("Beginning Fail Case: Incorrect credit card length")
        with self.client.post("http://localhost:8081/checkout", json={'user': {'name': 'nospace', 'contact': 'MK@MK.com'}, 'creditCard': {'number': '12890', 'expirationDate': '12/52', 'cvv': '123'}, 'userComment': '', 'items': [{'name': 'Learning Python', 'quantity': 1}], 'discountCode': '', 'shippingMethod': '', 'giftMessage': '', 'billingAddress': {'street': 'Ranna Tee 1', 'city': 'Tartu', 'state': 'County', 'zip': '51008', 'country': 'Estonia'}, 'giftWrapping': False, 'termsAndConditionsAccepted': True, 'notificationPreferences': ['email'], 'device': {'type': 'Smartphone', 'model': 'Samsung Galaxy S10', 'os': 'Android 10.0.0'}, 'browser': {'name': 'Chrome', 'version': '85.0.4183.127'}, 'appVersion': '3.0.0', 'screenResolution': '1440x3040', 'referrer': 'https://www.google.com', 'deviceLanguage': 'en-US'}, catch_response=True) as response:
            try:
                logging.info(response.json())
                if response.json()["status"] != "Order Rejected":
                    logging.info("Did not get expected value in status")
                    response.failure("Did not get expected value in status")
                else:
                    logging.info("Correct response to unsuccessful order")
                    response.success()
            except JSONDecodeError:
                logging.info("Could not be decoded as JSON")
                response.failure("Response could not be decoded as JSON")
            except KeyError:
                response.failure("Response did not contain expected key 'greeting'")

    @task
    def failReponseExpiration(self):
        logging.info("Beginning Fail Case: Expired Credit Card")
        with self.client.post("http://localhost:8081/checkout", json={'user': {'name': 'nospace', 'contact': 'MK@MK.com'}, 'creditCard': {'number': '12890', 'expirationDate': '5/19', 'cvv': '123'}, 'userComment': '', 'items': [{'name': 'Learning Python', 'quantity': 1}], 'discountCode': '', 'shippingMethod': '', 'giftMessage': '', 'billingAddress': {'street': 'Ranna Tee 1', 'city': 'Tartu', 'state': 'County', 'zip': '51008', 'country': 'Estonia'}, 'giftWrapping': False, 'termsAndConditionsAccepted': True, 'notificationPreferences': ['email'], 'device': {'type': 'Smartphone', 'model': 'Samsung Galaxy S10', 'os': 'Android 10.0.0'}, 'browser': {'name': 'Chrome', 'version': '85.0.4183.127'}, 'appVersion': '3.0.0', 'screenResolution': '1440x3040', 'referrer': 'https://www.google.com', 'deviceLanguage': 'en-US'}, catch_response=True) as response:
            try:
                logging.info(response.json())
                if response.json()["status"] != "Order Rejected":
                    logging.info("Did not get expected value in status")
                    response.failure("Did not get expected value in status")
                else:
                    logging.info("Correct response to unsuccessful order")
                    response.success()
            except JSONDecodeError:
                logging.info("Could not be decoded as JSON")
                response.failure("Response could not be decoded as JSON")
            except KeyError:
                response.failure("Response did not contain expected key 'greeting'")

    @task(3)
    def visitHome(self):
        logging.info("Visiting Home Page")
        self.client.get("/")

    @task
    def failResponseCVV(self):
        logging.info("Beginning Fail Case: CVV wrong length")
        with self.client.post("http://localhost:8081/checkout", json={'user': {'name': 'nospace', 'contact': 'MK@MK.com'}, 'creditCard': {'number': '12890', 'expirationDate': '5/19', 'cvv': '1211113'}, 'userComment': '', 'items': [{'name': 'Learning Python', 'quantity': 1}], 'discountCode': '', 'shippingMethod': '', 'giftMessage': '', 'billingAddress': {'street': 'Ranna Tee 1', 'city': 'Tartu', 'state': 'County', 'zip': '51008', 'country': 'Estonia'}, 'giftWrapping': False, 'termsAndConditionsAccepted': True, 'notificationPreferences': ['email'], 'device': {'type': 'Smartphone', 'model': 'Samsung Galaxy S10', 'os': 'Android 10.0.0'}, 'browser': {'name': 'Chrome', 'version': '85.0.4183.127'}, 'appVersion': '3.0.0', 'screenResolution': '1440x3040', 'referrer': 'https://www.google.com', 'deviceLanguage': 'en-US'}, catch_response=True) as response:
            try:
                logging.info(response.json())
                if response.json()["status"] != "Order Rejected":
                    logging.info("Did not get expected value in status")
                    response.failure("Did not get expected value in status")
                else:
                    logging.info("Correct response to unsuccessful order")
                    response.success()
            except JSONDecodeError:
                logging.info("Could not be decoded as JSON")
                response.failure("Response could not be decoded as JSON")
            except KeyError:
                response.failure("Response did not contain expected key 'greeting'")