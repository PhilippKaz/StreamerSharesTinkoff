import asyncio
from tinkoff.invest import Client

from config import ACCESS_TOKEN

def main():
    with Client(ACCESS_TOKEN) as client:
        r = client.instruments.shares()
        print(r.instruments[0])

if __name__ == '__main__':
    main()

