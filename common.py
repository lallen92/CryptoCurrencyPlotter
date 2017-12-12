import datetime
from GraphPlotter import Graph

'''
    CommonClass that is currently responsible for getting the past days days worth of data from the db. 
    This class will contain all the commonly used functions. More work needed!
'''
class CommonClass:

    def seven_days(self, data_list):
        """
            seven_days() - Gets the past 7 days worth of data.

            Parameters:
                - data_list: List of tuples containing the currencies value and the timestamp it was recorded.
            Returns:
                None
        """

        # The zip() function returns an iterator of tuples based on the iterable object.
        btceur_high, btceur_timestamp = zip(*data_list)

        # Various lists/variables used
        utc_btceur_timestamp = []
        one_week_list_timezone = []
        one_week_list_btc_high = []
        count = 0

        # Very inefficient! Only temporary. Database will grow, not practical to covert everything when only
        # want past 7 days
        for x in btceur_timestamp:
            utc_btceur_timestamp.append(datetime.datetime.fromtimestamp(x))

        # Get the latest entry to work back from
        orig = datetime.datetime.fromtimestamp(btceur_timestamp[-1])
        # Get a date 7 days from the current date
        one_week = orig - datetime.timedelta(days=7)

        # Loop backwards through the timestamps getting the past 7 days worth
        for I in reversed(utc_btceur_timestamp):
            if I > one_week:
                one_week_list_timezone.append(I)
            else:
                # Get the corresponding data to each time stamp
                for x in reversed(btceur_high):
                    if count < len(one_week_list_timezone):
                        one_week_list_btc_high.append(x)
                        count += 1

        # Temporary place holder for calling the plotter
        plotter = Graph()
        plotter.firstPlot(one_week_list_btc_high, one_week_list_timezone)
