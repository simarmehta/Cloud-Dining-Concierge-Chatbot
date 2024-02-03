import json
import boto3
import random
import logging
import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
region = 'us-east-1'
service = "es"
dynamodbTable = 'yelp_restaurants'
sqs_queue = "https://sqs.us-east-1.amazonaws.com/153437803668/Q1"
email_id = "sm11377@nyu.edu"
ES_URL = "https://search-restaurant-es-yz6gryc6wtcqpdj2cergutz37a.us-east-1.es.amazonaws.com"
username = "master1"
password = "Master@123"

def get_sqsQueueMessage():
    sqs = boto3.client('sqs')
    sqs_message = sqs.receive_message(QueueUrl=sqs_queue, MaxNumberOfMessages=1, MessageAttributeNames=['All'],
                                      VisibilityTimeout=0, WaitTimeSeconds=0)
    message = sqs_message['Messages'][0]
    logger.debug('Message Received from SQS Queue Q1={}'.format(message))
    return sqs, message


def get_slots(message):
    attributes = message['MessageAttributes']
    return attributes['Cuisine']['StringValue'], attributes['Location']['StringValue'], attributes['DiningDate'][
        'StringValue'], attributes['DiningTime']['StringValue'], attributes['NumberOfPeople']['StringValue'], \
    attributes['Email']['StringValue']


def connect_dynamoDBTable():
    db = boto3.resource('dynamodb')
    table = db.Table(dynamodbTable)
    return table


def get_restaurant_ids(cuisine):
    headers = {"Content-Type": "application/json"}
    query = {
        "size": 10,
        "query": {
            "match": {
                "cuisine_type": cuisine.lower()
            }
        }
    }
    response = requests.post(ES_URL + '/restindex/_search', auth=HTTPBasicAuth(username, password), headers=headers, json=query)

    if response.status_code != 200:
        return []

    data = response.json()
    restaurant_ids = [hit['_source']['id'] for hit in data['hits']['hits']]

    return restaurant_ids
    
def get_restaurant(table, restaurant_ids):
    restaurant_list = []

    for restaurant_id in restaurant_ids:
        response = table.get_item(
            Key={
                'id': restaurant_id 
            }
        )

        if 'Item' in response:
            restaurant_list.append(response['Item'])
    
    return restaurant_list


def get_message(restaurant_list, cuisine, location, date, dining_time, people, email):
    email_message = f"Here are a few {cuisine} cuisine recommendations in {location} for {people} people, on {date} at {dining_time}. <br><br>"
    for restaurant in restaurant_list:
        email_message = f"Here are a few {cuisine} cuisine recommendations in {location} for {people} people, on {date} at {dining_time}.<br><br>"

        for index, restaurant in enumerate(restaurant_list, 1):  
            email_message += f"{index}. Restaurant: {restaurant['name']}. It has {restaurant['review_count']} reviews with an average {restaurant['rating']} rating. The address is: {restaurant['address']}.<br><br>"

        email_message += f"Enjoy your meal!"

    return email_message


def send_email(email, email_message):
    ses = boto3.client('ses')
    response = ses.send_email(
        Source=email_id,
        Destination={'ToAddresses': [email]},
        ReplyToAddresses=[email_id],
        Message={
            'Subject': {'Data': 'Dining Conceirge Recommendations', 'Charset': 'utf-8'},
            'Body': {
                'Text': {'Data': email_message, 'Charset': 'utf-8'},
                'Html': {'Data': email_message, 'Charset': 'utf-8'}
            }
        }
    )


def delete_SQSEntry(sqs, sqs_queue, message):
    receipt_handle = message['ReceiptHandle']
    sqs.delete_message(QueueUrl=sqs_queue, ReceiptHandle=receipt_handle)
    
def connect_userinfoTable():
    db = boto3.resource('dynamodb')
    user_info_table = db.Table('user_info')
    return user_info_table
    
def store_user_recommendation(table, email, location, cuisine, restaurant_list):
    table.put_item(
        Item={
            'email': email,
            'location': location,
            'cuisine': cuisine,
            'recommendations': [restaurant['name'] for restaurant in restaurant_list]
        }
    )
    
   


def lambda_handler(event, context):
    sqs, message = get_sqsQueueMessage()
    cuisine, location, date, dining_time, people, email = get_slots(message)
    restaurant_ids = get_restaurant_ids(cuisine)
    
    table = connect_dynamoDBTable()
    restaurant_list = get_restaurant(table, restaurant_ids)
    
    email_message = get_message(restaurant_list, cuisine, location, date, dining_time, people, email)
    
    user_info_table = connect_userinfoTable()
    store_user_recommendation(user_info_table, email, location, cuisine, restaurant_list)
   
    send_email(email, email_message)
    delete_SQSEntry(sqs, sqs_queue, message)

    return {
        'statusCode': 200,
        'body': email_message
    }

