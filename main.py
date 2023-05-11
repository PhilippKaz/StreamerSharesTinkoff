import asyncio
from tinkoff.invest import Client

from config import ACCESS_TOKEN
from database import *


def main():
    with Client(ACCESS_TOKEN) as client:
        notParseShareList = client.instruments.shares()
        shareList = notParseShareList.instruments
        createShares(shareList)



if __name__ == '__main__':
    main()

