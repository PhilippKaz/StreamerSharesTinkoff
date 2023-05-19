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
    retry_settings = RetryClientSettings(use_retry=True, max_retry_attempt=2)
    with RetryingClient(ACCESS_TOKEN, settings=retry_settings) as client:
        for candle in client.get_all_candles(
                figi="BBG006L8G4H1",
                from_=now() - timedelta(days=1),
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        ):
            historyShareDetail = {}
            # Формирование детализации
            historyShareDetail['realPrice'] = convertToRealPrice(candle.open.units, candle.open.nano)
            historyShareDetail['unitsPrice'] = candle.open.units
            historyShareDetail['nanoPrice'] = candle.open.nano
            historyShareDetail['timeCandle'] = convertToRealDateTime(candle.time)
            
            # Формирование словаря
            historyShare[convertToTimeStamp(candle.time)] = historyShareDetail


        [last] = collections.deque(historyShare, maxlen=1)
        [first] = collections.deque(historyShare, maxlen=1)

        mAgo1 = last - (timedelta(minutes=1).total_seconds())
        mAgo5 = last - (timedelta(minutes=5).total_seconds())
        mAgo15 = last - (timedelta(minutes=15).total_seconds())
        mAgo30 = last - (timedelta(minutes=30).total_seconds())
        mAgo60 = last - (timedelta(minutes=60).total_seconds())
        hAgo4 = last - (timedelta(hours=4).total_seconds())
        hAgo8 = last - (timedelta(hours=8).total_seconds())
        hAgo24 = first


        shareNow = historyShare.get(last)
        shareMAgo1 = historyShare.get(mAgo1)
        shareMAgo5 = historyShare.get(mAgo5)
        shareMAgo15 = historyShare.get(mAgo15)
        shareMAgo30 = historyShare.get(mAgo30)
        shareMAgo60 = historyShare.get(mAgo60)
        shareHAgo4 = historyShare.get(hAgo4)
        shareHAgo8 = historyShare.get(hAgo8)
        shareHAgo24 = historyShare.get(hAgo24)

        print(getDiffPercent(shareNow['realPrice'], shareMAgo1['realPrice']))
        print(getDiffPercent(shareNow['realPrice'], shareMAgo5['realPrice']))
        print(getDiffPercent(shareNow['realPrice'], shareMAgo15['realPrice']))
        print(getDiffPercent(shareNow['realPrice'], shareMAgo30['realPrice']))
        print(getDiffPercent(shareNow['realPrice'], shareMAgo60['realPrice']))
        print(getDiffPercent(shareNow['realPrice'], shareHAgo4['realPrice']))
        print(getDiffPercent(shareNow['realPrice'], shareHAgo8['realPrice']))
        print(getDiffPercent(shareNow['realPrice'], shareHAgo24['realPrice']))










if __name__ == '__main__':
    main()
