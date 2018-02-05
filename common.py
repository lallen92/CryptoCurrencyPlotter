import datetime
from GraphPlotter import Graph


'''
    CommonClass that is currently responsible for getting the past days days worth of data from the db. 
    This class will contain all the commonly used functions. More work needed!
'''
class CommonClass(object):

    def length_of_data(self, data_list, days):
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
        one_week_list_timezone = []
        one_week_list_btc_high = []
        count = 0

        # Get the latest entry to work back from
        orig = datetime.datetime.fromtimestamp(btceur_timestamp[-1])
        # Get a date 7 days from the current date
        one_week = orig - datetime.timedelta(days=days)
        # Loop backwards through the timestamps getting the past 7 days worth

        for I in reversed(btceur_timestamp):
            converted_timestamp_value = (datetime.datetime.fromtimestamp(I))
            if one_week > converted_timestamp_value < orig:
                one_week_list_timezone.append(converted_timestamp_value)
            else:
                continue
        if one_week_list_timezone[-1] \
                > one_week:
            return None
        else:
            # Get the corresponding data to each time stamp
            for x in reversed(btceur_high):
                if count < len(one_week_list_timezone):
                    one_week_list_btc_high.append(x)
                    count += 1

            # Reorder both lists of data
            one_week_list_btc_high.reverse()
            one_week_list_timezone.reverse()
            zipped = zip(one_week_list_btc_high, one_week_list_timezone)
            return list(zipped)

