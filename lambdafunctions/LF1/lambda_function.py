import os
import time
import boto3
import datetime

from utils import *
from validations import *
from actions import pushInfoToSqs


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user_info')  

def get_greeting_intent(intent_request):
    session_attributes = intent_request.get('sessionState', {}).get('sessionAttributes', {})
    
    current_hour = datetime.datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    response_msg = f'{greeting}, What can I assist you with today?'
    
    return close(session_attributes, 'GreetingIntent', response_msg)


def get_goodbye_intent(intent_request):
    session_attributes = intent_request.get('sessionState', {}).get('sessionAttributes', {})
    return close(session_attributes, 'ThankYouIntent', 'Thank you for using Dining Conceirge Chatbot. Have a great day!')

def get_slot_value(slots, slot_name):
    if slot_name in slots:
        slot = slots[slot_name]
        if slot and 'value' in slot and 'interpretedValue' in slot['value']:
            return slot['value']['interpretedValue']
    return None

def get_existing_recommendation(email):
    response = table.get_item(
        Key={
            'email': email
        }
    )
    return response.get('Item')
    

def get_dining_suggestions_intent(intent_request):
    slots = intent_request['sessionState']['intent']['slots']

    cuisine = get_slot_value(slots, 'Cuisine')
    location = get_slot_value(slots, 'Location')
    dining_date = get_slot_value(slots, 'DiningDate')
    dining_time = get_slot_value(slots, 'DiningTime')
    people = get_slot_value(slots, 'NumberOfPeople')
    email = get_slot_value(slots, 'Email')
    continue_with = get_slot_value(slots, 'ContinueWithRecommendation')

    session_attributes = intent_request.get('sessionAttributes', {})
    
    if email and not continue_with:  
        existing_recommendation = get_existing_recommendation(email)
        if existing_recommendation:
            previous_cuisine = existing_recommendation.get('cuisine')
            previous_location=existing_recommendation['location']
            previous_recommendations = existing_recommendation.get('recommendations')
            recommendations_str = ', '.join(previous_recommendations)
            message = f'You searched for {previous_cuisine} cuisine previously in {previous_location}. These suggestions might interest you: {recommendations_str}. Do you want to proceed with a new set of recommendations?'
            return elicit_slot(session_attributes, intent_request['sessionState']['intent']['name'], slots, 'ContinueWithRecommendation', message)

    if continue_with:
        if continue_with.lower() == 'no':
            return close(session_attributes, 'DiningSuggestionsIntent', 'Thanks for confirming. Have a great meal!')
        
    if people:
        people = int(people)
    
    if intent_request['invocationSource'] == 'DialogCodeHook':
        invalid_slot = None
        invalid_message = None

        validations = [
            (cuisine, check_invalid_cuisine, 'Cuisine', 'This cuisine is not supported. Please provide another cuisine like chinese, indian, italian, etc.'),
            (location, check_invalid_location, 'Location', 'This location is not supported. Please provide another city like Manhattan.'),
            (dining_date, check_invalid_date, 'DiningDate', 'The entered date is invalid. Please make sure that your date is later than today.'),
            (dining_time, lambda x: check_invalid_time(x, dining_date), 'DiningTime', 'The entered time is invalid. Please make sure that your time is later than the current time.'),
            (people, check_invalid_people, 'NumberOfPeople', 'You can get suggestions for 1-20 people. Please provide a valid number.')
        ]

        for value, check_function, slot, message in validations:
            if value and check_function(value):
                invalid_slot = slot
                invalid_message = message
                break

        if invalid_slot:
            return elicit_slot(session_attributes, intent_request['sessionState']['intent']['name'], slots, invalid_slot, invalid_message)

        return delegate(session_attributes, slots)
        
    slot_values = [cuisine, location, dining_date, dining_time, people, email]
    sqs_response = pushInfoToSqs(slot_values)
    return close(session_attributes, 'DiningSuggestionsIntent', 'Thanks for the info. You will soon receive suggestions at {} !'.format(email))

def route_intent(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    print("Current intent name is:", intent_name)

    if intent_name == 'GreetingIntent':
        return get_greeting_intent(intent_request)

    elif intent_name == 'DiningSuggestionsIntent':
        return get_dining_suggestions_intent(intent_request)

    elif intent_name == 'ThankYouIntent':
        return get_goodbye_intent(intent_request)

def lambda_handler(event, context):
    print('Updated with Lex V2 main, debugging')
    os.environ["TZ"] = 'America/New_York'
    time.tzset()

    return route_intent(event)