import psycopg2
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Connect to your postgres DB
conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
def connectionToDb():
    try:
        print('Открытие соединения с БД')
        return conn.cursor()
    except Exception:
        print('Ошибка: '+Exception)
def createShares(shareList):
    cursorDb = connectionToDb()
    for i in range(len(shareList)):
        name = shareList[i].name.replace( "'", "")
        figi = shareList[i].figi
        ticker = shareList[i].ticker
        classCode = shareList[i].class_code
        isin = shareList[i].isin
        lot = shareList[i].lot
        currency = shareList[i].currency
        uid = shareList[i].uid
        positioUid = shareList[i].position_uid

        SQL = f'INSERT INTO public."Z_SHARES"("NAME", "TICKER", "FIGI", "CLASS_CODE", "ISIN", "LOT", "CURRENCY", "UID", "POSITION_UID") ' \
               f'''VALUES ('{name}','{ticker}','{figi}','{classCode}','{isin}',{lot},'{currency}','{uid}','{positioUid}');''';
        cursorDb.execute(SQL)
        conn.commit()


    clostConnectionDb(cursorDb)


def getShareRub():
    cursorDb = connectionToDb()
    SQL =f'''select * from public."Z_SHARES" where "CURRENCY" = 'rub'''+"'"
    cursorDb.execute(SQL)
    listShare = cursorDb.fetchall()
    clostConnectionDb(cursorDb)
    return listShare



def clostConnectionDb(cursorClose):
    print('Закрытие соединения с БД')
    cursorClose.close()
    conn.close()


