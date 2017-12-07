import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

class Graph(object):
    def firstPlot(self, btceur_high, btceur_timestamp):

        fig, ax = plt.subplots()
        # Plot the date using plot_date rather than plot

        # Convert to the correct format for matplotlib.
        # mdate.epoch2num converts epoch timestamps to the right format for matplotlib
        secs = mdate.epoch2num(btceur_timestamp)
        print (secs)
        ax.plot_date(secs, btceur_high, color="blue", linewidth=1.0, linestyle="-")

        # Choose your xtick format string
        date_fmt = '%d'

        # Use a DateFormatter to set the data to the correct format.
        date_formatter = mdate.DateFormatter(date_fmt)
        ax.xaxis.set_major_formatter(date_formatter)

        # Sets the tick labels diagonal so they fit easier.
        fig.autofmt_xdate()


        #plt.plot(btceur_timestamp, btceur_high, color="blue", linewidth=1.0, linestyle="-")

        # Set x limits
        #plt.xlim(-4.0,4.0)

        # Set x ticks
       # plt.xticks(np.linspace(-4,4,9,endpoint=True))

        # Set y limits
        #plt.ylim(-1.0,1.0)

        # Set y ticks
        #plt.yticks(np.linspace(-1,1,5,endpoint=True))

        # Save figure using 72 dots per inch
        # savefig("../figures/exercice_2.png",dpi=72)

        # Show result on screen
        plt.show()

