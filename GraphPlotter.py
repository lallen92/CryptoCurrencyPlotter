import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

class Graph(object):
    def firstPlot(self, btceur_high, btceur_timestamp):

        # Create a new figure of size 8x6 points, using 100 dots per inch
        fig, ax = plt.subplots()
        # Convert to the correct format for matplotlib.
        # mdate.epoch2num converts epoch timestamps to the right format for matplotlib
        # x = mdate.epoch2num(btceur_timestamp)

        # Choose your xtick format string
        date_fmt = '%d'

        # Use a DateFormatter to set the data to the correct format.
        date_formatter = mdate.DateFormatter(date_fmt)
        ax.xaxis.set_major_formatter(date_formatter)

        # Sets the tick labels diagonal so they fit easier.
        fig.autofmt_xdate()
        fig.subplots_adjust(hspace=5)

        # Plot BTC/EUR using blue color with a continuous line of width 1 (pixels)
        ax.plot(btceur_timestamp, btceur_high, color="blue", linewidth=1.0, linestyle="-")

        # Show result on screen
        plt.show()
