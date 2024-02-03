import datetime
import dateutil.parser

def check_invalid_date(date):
    try:
        input_date = dateutil.parser.parse(date).date()
        if input_date < datetime.date.today():
            return True
        return False
    except ValueError:
        return False

def check_invalid_time(time, date):
    try:
        input_time = dateutil.parser.parse(time).timestamp()
        input_date = dateutil.parser.parse(date).date()
        if input_date == datetime.date.today() and input_time < datetime.datetime.now().timestamp():
            return True
        return False
    except ValueError:
        return False
        
def check_invalid_cuisine(cuisine):
    cuisines = ['indian','italian','mexican','chinese','japanese','french','greek']
    return cuisine.lower() not in cuisines

def check_invalid_location(location):
    return location.lower() != 'manhattan'

def check_invalid_people(people):
    return people < 1 or people > 20
    
  