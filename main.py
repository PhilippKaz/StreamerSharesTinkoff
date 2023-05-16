import os
import time
from datetime import timedelta
import logging


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

# logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)


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
    retry_settings = RetryClientSettings(use_retry=True, max_retry_attempt=2)
    i = 0
    candleShareDict = {}
    with RetryingClient(ACCESS_TOKEN, settings=retry_settings) as client:
        for candle in client.get_all_candles(
                figi="BBG005D1WCQ1",
                from_=now() - timedelta(days=1),
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        ):
            i += 1
            candleShareDict = {'id':i,'time': (candle.time + timedelta(hours=3)).strftime('%d.%m.%Y-%H:%M:%S')}

            # print((candle.time + timedelta(hours=3)).strftime('%d.%m.%Y-%H:%M:%S'))
            # print(float(str(candle.open.units) + "." + str(candle.open.nano)))
        print(candleShareDict.items())


    # streamingShares('BBG005D1WCQ1')



if __name__ == '__main__':
    main()

