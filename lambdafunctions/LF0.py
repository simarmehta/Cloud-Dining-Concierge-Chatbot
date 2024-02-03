import boto3
import uuid
import datetime
    
def lambda_handler(event, context):
    text = (event.get("messages")[0].get("unstructured").get("text"))
    print('Input from user is: ', text)
    
    session_id = "s1"
    print('session_id is: ', session_id)
    
    client = boto3.client('lexv2-runtime')
    response = client.recognize_text(
        botId='I5XGNKTUYG',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId=session_id,
        text=text
    )
    print('Response is: ', response)

    
    UnstructuredMessage = {
        "id" : "1",
        # "text" : "I’m still under development. Please come back later.",
        "text" : response.get("messages")[0].get("content"),
        "timestamp" : str(datetime.datetime.now().timestamp())
    }
    
    Message = {
        "type" : "unstructured",
        "unstructured" : UnstructuredMessage
    }
    
    botResponse = {
        'statusCode': 200,
        "messages": [Message]
        
    }
    
    
    return botResponse
    
    
    
    
    


