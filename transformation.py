
from datetime import timedelta, datetime
def convertToRealDateTime(dateTime):
    return (dateTime + timedelta(hours=3)).strftime('%d.%m.%Y-%H:%M:%S')

def convertToRealPrice(unitPrice, nanoPrice):
    return float(str(unitPrice) + "." + str(nanoPrice))

def convertToTimeStamp(utcDateTime):
    return int(datetime.timestamp(utcDateTime))

def getDiffPercent(priceNowList, priceAgoList, percentDiff):
    if priceNowList is None:
        return;

    if priceAgoList is None:
        return;

    priceNow = priceNowList['realPrice']
    priceAgo = priceAgoList['realPrice']

    difference = priceNow - priceAgo

    if difference > 0:
        difference = (difference / priceAgo) * 100
        if abs(percentDiff) >= difference: return difference
    elif difference < 0:
        difference = (difference / priceNow) * 100
        if abs(percentDiff) >= difference: return difference

    elif difference == 0:
        return 0



