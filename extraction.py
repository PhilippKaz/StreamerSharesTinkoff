import collections
from datetime import timedelta


def extractDiff(exctractHistoryData):
    historyShareDiff = {}
    historyShareDiff_Detail = {}
    shareNowPrice = exctractHistoryData['shareNow']['realPrice']
    nameShare = exctractHistoryData['shareNow']['name']
    tickerShare = exctractHistoryData['shareNow']['ticker']
    lotShare = exctractHistoryData['shareNow']['lot']

    for key in exctractHistoryData.keys():
        historyShareDiff_Detail = {}
        realPriceTimeAgo = exctractHistoryData[key]['realPrice']
        diffPrice = shareNowPrice - realPriceTimeAgo

        if (diffPrice) > 0:
            if shareNowPrice != 0:
                diffPercent = (diffPrice/shareNowPrice)*100
        elif (diffPrice) < 0:
            if realPriceTimeAgo != 0:
                diffPercent = (diffPrice/realPriceTimeAgo)*100
        elif (diffPrice == 0):
            diffPercent = 0

        historyShareDiff_Detail['name'] = nameShare
        historyShareDiff_Detail['ticker'] = tickerShare
        historyShareDiff_Detail['lot'] = lotShare
        historyShareDiff_Detail['FIGI'] = exctractHistoryData[key]['FIGI']
        historyShareDiff_Detail['realPrice'] = realPriceTimeAgo
        historyShareDiff_Detail['diffPrice'] = diffPrice
        historyShareDiff_Detail['diffPercent'] = diffPercent
        historyShareDiff_Detail['unitsPrice'] = exctractHistoryData[key]['unitsPrice']
        historyShareDiff_Detail['nanoPrice'] = exctractHistoryData[key]['nanoPrice']
        historyShareDiff_Detail['timeCandle'] = exctractHistoryData[key]['timeCandle']

        historyShareDiff[key] = historyShareDiff_Detail

        # str_kek = 'realPrice: ' + str(realPriceTimeAgo)  + ' - shareNowPrice: ' + str(shareNowPrice) + ' - diffPrice: ' + str(diffPrice) + ' -diffPercent: ' + str(diffPercent)

    return historyShareDiff


def extractionHistoryData(historyShare):
    dictHistory = {}
    diffHistoryList = {}
    exctractHistoryData = {}
    [last] = collections.deque(historyShare, maxlen=1)
    [first] = collections.deque(historyShare, maxlen=1)

    mAgo1 = last - (timedelta(minutes=1).total_seconds())
    mAgo5 = last - (timedelta(minutes=5).total_seconds())
    mAgo15 = last - (timedelta(minutes=15).total_seconds())
    mAgo30 = last - (timedelta(minutes=30).total_seconds())
    mAgo60 = last - (timedelta(minutes=60).total_seconds())
    hAgo4 = last - (timedelta(hours=4).total_seconds())
    hAgo8 = last - (timedelta(hours=8).total_seconds())

    shareNow = historyShare.get(last)
    shareMAgo1 = historyShare.get(mAgo1)
    shareMAgo5 = historyShare.get(mAgo5)
    shareMAgo15 = historyShare.get(mAgo15)
    shareMAgo30 = historyShare.get(mAgo30)
    shareMAgo60 = historyShare.get(mAgo60)
    shareHAgo4 = historyShare.get(hAgo4)
    shareHAgo8 = historyShare.get(hAgo8)
    shareHAgo24 = historyShare.get(first)

    dictHistory['shareNow'] = shareNow
    dictHistory['shareMAgo1'] = shareMAgo1
    dictHistory['shareMAgo5'] = shareMAgo5
    dictHistory['shareMAgo15'] = shareMAgo15
    dictHistory['shareMAgo30'] = shareMAgo30
    dictHistory['shareMAgo60'] = shareMAgo60
    dictHistory['shareHAgo4'] = shareHAgo4
    dictHistory['shareHAgo8'] = shareHAgo8
    dictHistory['shareHAgo24'] = shareHAgo24

    # Чистим словарь от None
    exctractHistoryData = {key:value for key, value in dictHistory.items() if value is not None}

    diffHistoryData = extractDiff(exctractHistoryData)

    for shareDiff in diffHistoryData.keys():
        ticker = diffHistoryData[shareDiff]['ticker']
        diffPrice = format(diffHistoryData[shareDiff]['diffPrice'], '.10')
        time = diffHistoryData[shareDiff]['timeCandle']

        if (float(diffPrice)) > 1:
            message = '#'+ticker+' Изменение: '+str(diffPrice) + '% Время: ' + str(time)
            print(message)
