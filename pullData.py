#!/usr/bin/python3

import requests, logging, datetime
from dbConnector import MySQLConnector

'''
	Supported values for currency_pair: btcusd, btceur, eurusd, 
	xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc, ethusd, etheur, ethbtc 
'''


def dbCommit(table, fieldList, valueList):
    """
        dbCommit() - Writes the values pulled from 'www.bitstamp.net' to the the database

        Parameters:
            - table: Passes the relevant table name i.e. btceur, ethusd, etc...
            - fieldList: The list of column names used in the database
            - valueList: The values that correspond to each column name
        Returns:
            None
    """
    logger = logging.getLogger(__name__)

    dbConn = None
    dbConn = MySQLConnector()

    logger.info("Calling the WriteToDB function...")
    dbConn.writeToDB(table=table, fieldList=fieldList, valueList=valueList)


def main():
    """
        main() - Gets the values from 'www.bitstamp.net', extracts them from the returned dictionary and writes them to a database
        Parameters:
            - None
        Returns:
            - None
    """
    logger = logging.getLogger(__name__)

    currencyList = ['https://www.bitstamp.net/api/v2/ticker_hour/btceur', 'https://www.bitstamp.net/api/v2/ticker_hour/btcusd',
                    'https://www.bitstamp.net/api/v2/ticker_hour/ethusd', 'https://www.bitstamp.net/api/v2/ticker_hour/etheur']

    for currency in currencyList:
        res = requests.get(currency)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Not 200
            logger.error(str(e))
            continue

        currencyType = (currency.rpartition('/')[-1])
        logger.info('The Curreny type: ' + currencyType)

        if currencyType == 'btceur':
            table = 'btceur'
        elif currencyType == 'btcusd':
            table = 'btcusd'
        elif currencyType == 'ethusd':
            table = 'ethusd'
        elif currencyType == 'etheur':
            table = 'etheur'
        else:
            table = None

        # Extract Data and Fields
        data = res.json()
        fieldList = data.keys()
        logger.info(fieldList)
        valueList = data.values()
        logger.info(valueList)

        # Write to DB
        dbCommit(table, fieldList, valueList)


if __name__ == "__main__":
    # Configure the logger
    logfile = 'logfile_' + datetime.datetime.now().strftime("%A, %d. %B %Y %I-%M%p")
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filemode='w',
                        filename=logfile)

    logger = logging.getLogger(__name__)
    logger.info("Launching Application..")

    main()

