#!/usr/bin/python3

import requests, logging, datetime, threading, time
from dbConnector import MySQLConnector
from GraphPlotter import Graph

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


def pullData(stop_event):
    """
        pullData() - Gets the values from 'www.bitstamp.net', extracts them from the returned dictionary and writes them to a database
                     This in emcompassed in a seperate thread to the main program so that it can constantly pull data and write it to
                     the database while the program is contiuning to carry out its tasks
        Parameters:
            - stop_event: This can be used to cleanly terminate the child thread if its needs to be done before the parent is terminated
        Returns:
            - None
    """
    logger = logging.getLogger(__name__)

    dbConn = None
    dbConn = MySQLConnector()

    # List of current formats supported
    currencyList = ['https://www.bitstamp.net/api/v2/ticker_hour/btceur', 'https://www.bitstamp.net/api/v2/ticker_hour/btcusd',
                    'https://www.bitstamp.net/api/v2/ticker_hour/ethusd', 'https://www.bitstamp.net/api/v2/ticker_hour/etheur']

    # Loop until told otherwise!
    while not stop_event.is_set():
        for currency in currencyList:
            res = requests.get(currency)
            try:
                res.raise_for_status()
            except requests.exceptions.HTTPError as e:
                # Not 200
                logger.error(str(e))
                continue

            # Get the end characters to dertermine the type e.g. btceur, ethusd, etc...
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
        # Cannot make more than 600 requests per 10 minutes or they will ban your IP address.
        # Will in time get real time using their websocket API.
        time.sleep(5)
def main():
    # Start the thread
    stop_event= threading.Event()
    thread = threading.Thread(target=pullData, args=(stop_event,))
    thread.daemon = True                            # Daemonize thread
    thread.start()                                  # Start the execution


    db_read = MySQLConnector()

    field = "high,timestamp".split(",")
    data_list = db_read.readFromDB(table="btceur", fieldList=field)
    btceur_high, btceur_timestamp = zip(*data_list)

    plotter = Graph()
    plotter.firstPlot(btceur_high, btceur_timestamp)
    # stop_event.set()

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

