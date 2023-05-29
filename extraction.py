from datetime import timedelta

import telebot

from config import TOKEN_BOT, CHAT_ID

bot = telebot.TeleBot(TOKEN_BOT)

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
    message = ''
    dictHistory = {}
    diffHistoryList = {}
    exctractHistoryData = {}

    first_key, first_value = next(iter(historyShare.items()))
    last_key, last_value = next(iter(reversed(historyShare.items())))

    mAgo1 = last_key - (timedelta(minutes=1).total_seconds())
    mAgo5 = last_key - (timedelta(minutes=5).total_seconds())
    mAgo15 = last_key - (timedelta(minutes=15).total_seconds())
    mAgo30 = last_key - (timedelta(minutes=30).total_seconds())
    mAgo60 = last_key - (timedelta(minutes=60).total_seconds())
    hAgo4 = last_key - (timedelta(hours=4).total_seconds())
    hAgo8 = last_key - (timedelta(hours=8).total_seconds())

    shareNow = historyShare.get(last_key)
    shareMAgo1 = historyShare.get(mAgo1)
    shareMAgo5 = historyShare.get(mAgo5)
    shareMAgo15 = historyShare.get(mAgo15)
    shareMAgo30 = historyShare.get(mAgo30)
    shareMAgo60 = historyShare.get(mAgo60)
    shareHAgo4 = historyShare.get(hAgo4)
    shareHAgo8 = historyShare.get(hAgo8)
    shareHAgo24 = historyShare.get(first_key)

    dictHistory['shareNow'] = shareNow
    dictHistory['shareMAgo1'] = shareMAgo1
    dictHistory['shareMAgo5'] = shareMAgo5
    # dictHistory['shareMAgo15'] = shareMAgo15
    # dictHistory['shareMAgo30'] = shareMAgo30
    # dictHistory['shareMAgo60'] = shareMAgo60
    # dictHistory['shareHAgo4'] = shareHAgo4
    # dictHistory['shareHAgo8'] = shareHAgo8
    # dictHistory['shareHAgo24'] = shareHAgo24

    # Чистим словарь от None
    exctractHistoryData = {key:value for key, value in dictHistory.items() if value is not None}

    diffHistoryData = extractDiff(exctractHistoryData)

    for shareDiff in diffHistoryData.keys():
        ticker = diffHistoryData[shareDiff]['ticker']
        diffPercent = diffHistoryData[shareDiff]['diffPercent']
        time = diffHistoryData[shareDiff]['timeCandle']

        if (abs(float(diffPercent))) > 1:
            message = '#'+ticker+' Изменение: '+str(diffPercent) + '% Время: ' + str(time) + '\n' + message

    if len(message) > 0:
        bot.send_message(CHAT_ID, message)

