def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message_content):
    slots[slot_to_elicit] = None
    response = {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'intent': {
                'name': intent_name,
                'state': 'InProgress',
                'slots': slots
            },
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit
            }
        },
        'messages': [{
            'contentType': 'PlainText',
            'content': message_content
        }]
    }
    
    return response
    
def close(session_attributes, intent_name, message_content):
    print('Inside close')
    print('session_attributes -> ', session_attributes, ' intent_name -> ', intent_name, 'message_content', message_content)
    response = {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': {
                'name': intent_name,
                'state': 'Fulfilled',
            }
        },
        'messages': [{
            'contentType': 'PlainText',
            'content': message_content
        }]
    }
    return response
    
def delegate(session_attributes, slots):
    print('Inside delegate')
    print('session_attributes -> ', session_attributes, ' slots -> ', slots)
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'intent': {
                'name': 'DiningSuggestionsIntent',
                'state': 'InProgress',
                'slots': slots
            },
            'dialogAction': {
                'type': 'Delegate'
            }
        }
    }