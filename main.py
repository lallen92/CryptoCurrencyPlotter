import logging, datetime, threading
from dbConnector import MySQLConnector
from pullData import pull_data
from common import CommonClass


def main():
    # Start the thread, this is responsible for getting data and posting to db
    stop_event= threading.Event()
    thread = threading.Thread(target=pull_data, args=(stop_event,))
    thread.daemon = True                            # Daemonize thread
    thread.start()                                  # Start the execution

    db_read = MySQLConnector()
    days_data = CommonClass()

    field = "high,timestamp".split(",")
    data_list = db_read.readFromDB(table="btceur", fieldList=field)

    days_data.seven_days(data_list)

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
