
from datetime import timedelta, datetime
def convertToRealDateTime(dateTime):
    return (dateTime + timedelta(hours=3)).strftime('%d.%m.%Y-%H:%M:%S')

def convertToRealPrice(unitPrice, nanoPrice):
    return float(str(unitPrice) + "." + str(nanoPrice))

def convertToTimeStamp(utcDateTime):
    return int(datetime.timestamp(utcDateTime))