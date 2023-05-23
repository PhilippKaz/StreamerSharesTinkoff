from tinkoff.invest import (Client)
from database import *
from config import ACCESS_TOKEN


# Функция добавления акций в БД
def createShareList():
    with Client(ACCESS_TOKEN) as client:
        notParseShareList = client.instruments.shares()
        shareList = notParseShareList.instruments
        createShares(shareList)