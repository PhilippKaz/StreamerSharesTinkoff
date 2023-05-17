import time
import collections
import datetime



from tinkoff.invest import (
    CandleInstrument,
    Client,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

from tinkoff.invest import CandleInterval
from tinkoff.invest.retrying.settings import RetryClientSettings
from tinkoff.invest.retrying.sync.client import RetryingClient
from tinkoff.invest.utils import now

from config import ACCESS_TOKEN
from database import createShares
from transformation import *



# Функция добавления акций в БД
def createShareList():
    with Client(ACCESS_TOKEN) as client:
        notParseShareList = client.instruments.shares()
        shareList = notParseShareList.instruments
        createShares(shareList)

# Подписка на стоимость акцию (данные обновляются каждую минуту)
def streamingShares(shareFIGI):
    def requestIterator():
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                waiting_close=True,
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[CandleInstrument(
                                # figi="BBG005D1WCQ1",
                                figi=shareFIGI,
                                interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                            )
                        ],
            )
        )
        while True:
            time.sleep(1)
    with Client(ACCESS_TOKEN) as client:
        for marketdata in client.market_data_stream.market_data_stream(
                requestIterator()
        ):
            print(marketdata)


def main():
    historyShare = {}
    historyShareDetail = {}
    retry_settings = RetryClientSettings(use_retry=True, max_retry_attempt=2)
    with RetryingClient(ACCESS_TOKEN, settings=retry_settings) as client:
        for candle in client.get_all_candles(
                figi="BBG004S68JR8",
                from_=now() - timedelta(days=1),
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        ):
            historyShareDetail['realPrice'] = convertToRealPrice(candle.open.units, candle.open.nano)
            historyShareDetail['unitsPrice'] = candle.open.units
            historyShareDetail['nanoPrice'] = candle.open.units
            # historyShareDetail['timeCandle'] = convertToRealDateTime(candle.time)


            historyShare[convertToTimeStamp(candle.time)] = historyShareDetail

        [last] = collections.deque(historyShare, maxlen=1)

        print(type(last))

        # minutesAgo1 = candle - timedelta(minutes=1)
        # minutesAgo5 = last - timedelta(minutes=5)
        # minutesAgo15 = last - timedelta(minutes=15)
        # minutesAgo30 = last - timedelta(minutes=30)
        # minutesAgo60 = last - timedelta(minutes=60)
        # hoursAgo4 = last - timedelta(hours=4)
        # hoursAgo8 = last - timedelta(hours=8)
        # hoursAgo24 = last - timedelta(hours=24)

        # print(minutesAgo5)
        # print(minutesAgo15)
        # print(minutesAgo30)
        # print(minutesAgo60)
        # print(hoursAgo4)
        # print(hoursAgo8)
        # print(hoursAgo24)







            # print(convertToRealDateTime(candle.time))
            # print(convertToRealPirce(candle.open.units, candle.open.nano))







if __name__ == '__main__':
    main()

