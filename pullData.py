#!/usr/bin/python3

import requests
import logging
import time
from dbConnector import MySQLConnector

'''
	Supported values for currency_pair: btcusd, btceur, eurusd, 
	xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc, ethusd, etheur, ethbtc 
'''


def db_commit(table, field_list, value_list):
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
    db_conn = MySQLConnector()

    logger.info("Calling the WriteToDB function...")
    db_conn.writeToDB(table=table, fieldList=field_list, valueList=value_list)


def pull_data(stop_event):
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

    # List of current formats supported
    currency_list = ['https://www.bitstamp.net/api/v2/ticker_hour/btceur', 'https://www.bitstamp.net/api/v2/ticker_hour/btcusd',
                    'https://www.bitstamp.net/api/v2/ticker_hour/ethusd', 'https://www.bitstamp.net/api/v2/ticker_hour/etheur']

    # Loop until told otherwise!
    while not stop_event.is_set():
        for currency in currency_list:
            res = requests.get(currency)
            try:
                res.raise_for_status()
            except requests.exceptions.HTTPError as e:
                # Not 200
                logger.error(str(e))
                continue

            # Get the end characters to dertermine the type e.g. btceur, ethusd, etc...
            currency_type = (currency.rpartition('/')[-1])
            logger.info('The Curreny type: ' + currency_type)

            if currency_type == 'btceur':
                table = 'btceur'
            elif currency_type == 'btcusd':
                table = 'btcusd'
            elif currency_type == 'ethusd':
                table = 'ethusd'
            elif currency_type == 'etheur':
                table = 'etheur'
            else:
                table = None

            # Extract Data and Fields
            data = res.json()
            field_list = data.keys()
            logger.info(field_list)
            value_list = data.values()
            logger.info(value_list)

            # Write to DB
            db_commit(table, field_list, value_list)
        # Cannot make more than 600 requests per 10 minutes or they will ban your IP address.
        # Will in time get real time using their websocket API.
        time.sleep(5)


