import time
import telebot


from tinkoff.invest import CandleInterval
from tinkoff.invest.retrying.settings import RetryClientSettings
from tinkoff.invest.retrying.sync.client import RetryingClient
from tinkoff.invest.utils import now

from config import ACCESS_TOKEN
from transformation import *
from database import *
from extraction import *

# Формирование исторического массива данных
def getHistoryShare(shareList):
    historyShare = {}
    retry_settings = RetryClientSettings(use_retry=True, max_retry_attempt=2)
    with RetryingClient(ACCESS_TOKEN, settings=retry_settings) as client:
        for candle in client.get_all_candles(
                figi=shareList[3],
                from_=now() - timedelta(days=1),
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        ):
            historyShareDetail = {}
            # Формирование детализации
            historyShareDetail['name'] = shareList[1]
            historyShareDetail['ticker'] = shareList[2]
            historyShareDetail['FIGI'] = shareList[3]
            historyShareDetail['lot'] = shareList[6]
            historyShareDetail['realPrice'] = convertToRealPrice(candle.open.units, candle.open.nano)
            historyShareDetail['unitsPrice'] = candle.open.units
            historyShareDetail['nanoPrice'] = candle.open.nano
            historyShareDetail['timeCandle'] = convertToRealDateTime(candle.time)

            # Формирование словаря
            historyShare[convertToTimeStamp(candle.time)] = historyShareDetail

    return historyShare

def streamingShareOnline():
    shareList = getShareRub()

    while True:
        for share in shareList:
            try:
                historyShare = getHistoryShare(share)
                if len(historyShare) > 0:
                    if historyShare is not None:
                        extractionHistoryData(historyShare)
                        time.sleep(1.2)
            except Exception as error:
                print(error)
                continue
            finally:
                continue

def main():
    streamingShareOnline()

if __name__ == '__main__':
    main()
