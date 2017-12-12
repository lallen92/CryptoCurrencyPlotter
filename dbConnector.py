import pymysql, logging
'''
    SQLClass that is responsible for establishing a connection to the database and as of now, for writing to the database
'''
class MySQLConnector(object):
    def __init__(self, serverName="localhost", port=None, dbName="project_one", username="root", password=""):
        '''
            MySQLConnector() - Constructor

            Parameters:
                - serverName: the name or IP address of the database server to connect to.
                - port: the port on which the MySQL database is listening.
                - dbName: The name of the database to associate with this Connection
                - username: the username to log on with
                - password: the password to log on with
            Returns:
                - None
		'''
        self.serverName = serverName
        self.port = port
        self.dbName = dbName
        self.username = username
        self.password = password

        logger = logging.getLogger(__name__)
        logger.info("Checking connection...")
        try:
            self.checkConnection()
        except:
            logger.error("Failed to Connect...")

    def checkConnection(self):
        '''
		    checkConnection() - checks that this connection object can connect to the specified database

		    Parameters:
			    None

		    Returns:
			    - bool: True if connection is successful, False otherwise
		'''
        logger = logging.getLogger(__name__)

        try:
            conn = self.getConnection()
        except Exception as e:
            logger.error(("Can't connect to MySQL database at %s:%d/%s with details given. Error: %s" %
                                       (self.serverName, self.port, self.dbName, str(e))))
        conn.close()

    def getConnection(self):
        '''
            writeToDB() - writes to the specified table, for the specified fieldlist the values provided, as one row entry to the DB

            Parameters:
                - None
            Returns:
                - Connection to DB
		'''
        return pymysql.connect(host=self.serverName, port=self.port, user=self.username, passwd=self.password,
                               db=self.dbName)

    def writeToDB(self, table, fieldList, valueList):
        '''
            writeToDB() - writes to the specified table, for the specified fieldlist the values provided, as one row entry to the DB

            Parameters:
                - table: A string containing the name of the table in the database
                - fieldlist: A list of strings representing the column names in the database table
                - valuelist: A list of strings representing the values to be written into the row in the database
            Returns:
                - None
		'''
        logger = logging.getLogger(__name__)

        if len(fieldList) != len(valueList):
            logger.error("The list of arguments to write to the DB should be %d items long, but is instead %d long. The list of column names" \
                        " is as follows: %s" % (len(fieldList), len(valueList), str(fieldList)))

        db = self.getConnection()
        query = "INSERT INTO `%s` (`%s`) VALUES (\"%s\");" % (
            table, "`, `".join([str(x) for x in fieldList]), "\", \"".join([str(x) for x in valueList]))

        logger.info("The query being commited: %s" % query)
        cur = db.cursor()

        # Execute the SQL command
        try:
            cur.execute(query)
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            logger.error("Write failed...Rolling back!!")

        if cur.rowcount <= 0:
            logger.error("Write failed. Query: %s" % query)

        db.close()


    def readFromDB(self, fieldList, table):
        '''
		    readFromDB() - reads from the specified table the columns (specified by fieldlist), filtering by the condition, order and limit
		 	        	   when supplied

		    Parameters:
			    - table: A string containing the name of the table in the database
			    - fieldlist: A list of strings containing the column names to read in the database table
		    Returns:
			    - results: a tuple of tuples (get that!) or 2D array of results, representing rows in the database that match your query
        '''
        logger = logging.getLogger(__name__)

        query = "SELECT `%s` FROM `%s`" % ("`, `".join(fieldList), table)
        logger.info("The query being read: %s" % query)

        db = self.getConnection()
        cur = db.cursor()
        cur.execute(query)

        results = cur.fetchall()
        db.close()

        return results

    def close(self):
        '''
            close() - closes the database connector, removing the connection pool

            Parameters:
                None

            Returns:
                None
        '''

        self.close()
