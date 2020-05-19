import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
from os import getcwd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def main():
    path = getcwd() + '/datetime.csv'
    date_df = pd.read_csv(path) # reading from the csv file
    print(date_df['date'])
    #x_axis = pd.to_datetime(date_df['date'])
    #plt.hist(x_axis, bins=10)

    # turning the column with the date into datetime64 format
    date_df['date'] = date_df['date'].astype('datetime64')
    # classifying users on their specializations to get multi stats
    for z in range(len(date_df)):
        if date_df.at[z, 'specialization'] == 'STARTUP':
            date_df.at[z, 'startup'] = 1
        elif date_df.at[z, 'specialization'] == 'MENTOR':
            date_df.at[z, 'mentor'] = 1
        elif date_df.at[z, 'specialization'] == 'PARTNER':
            date_df.at[z, 'partner'] = 1
    try:
        date_df[['startup', 'mentor', 'partner']].groupby([date_df['date'].dt.day, # visualizing the data
                                                           date_df['date'].dt.month]).count().plot(kind="bar")
        plt.savefig('graph.png', bbox_inches='tight') # saving the visualized data to the png file
    except TypeError:
        pass


if __name__ == '__main__':
    main()
