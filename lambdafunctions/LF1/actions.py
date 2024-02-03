import boto3

def pushInfoToSqs(slot_values):
    sqs_client = boto3.client('sqs')
    queue_url = "https://sqs.us-east-1.amazonaws.com/153437803668/Q1"

    response = sqs_client.send_message(
        QueueUrl=queue_url,
        # DelaySeconds=10,
        MessageAttributes={
            'Cuisine': {
                'DataType': 'String',
                'StringValue': slot_values[0]
            },
            'Location': {
                'DataType': 'String',
                'StringValue': slot_values[1]
            },
            'DiningDate': {
                'DataType': 'String',
                'StringValue': slot_values[2]
            },
            'DiningTime': {
                'DataType': 'String',
                'StringValue': slot_values[3]
            },
            'NumberOfPeople': {
                'DataType': 'Number',
                'StringValue': "{}".format(slot_values[4])
            },
            'Email': {
                'DataType': 'String',
                'StringValue': slot_values[5]
            }
        },
        MessageBody=(
            'User Input'
        )
    )
    return response