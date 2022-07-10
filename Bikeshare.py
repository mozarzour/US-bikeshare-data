import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York or Washington?\n').lower()
        if city not in ['chicago','new york city', 'washington']:
            print('Please enter on of the three available cities.\n')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    month_filter = ''
    while month_filter not in ['y','n']:
        month_filter=input('Do you want a specific month? Y or N\n').lower()
        if month_filter == 'y':
            while True:
                month = input('Which month? January, February, March, April, May or June? Type the full month name.\n').lower()
                if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                    print('please enter the full month name\n')
                    continue
                else:
                    break
                break
        elif month_filter == 'n':
            month = 'all'
            break
        else:
            print('Please enter y for yes and n for no')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_filter = ''
    while day_filter not in ['y','n']:
        day_filter = input('Do you want a specific day? Y or N\n').lower()
        if day_filter == 'y':
            while True:
                day = input('Which day? Please Type the full day name.\n').lower()
                if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                    print('Please enter the full day name\n')
                    continue
                else:
                    break
            break
        elif day_filter == 'n':
            day = 'all'
            break
        else:
            print('Please enter y for Yes and n for No')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month
    df['Day']=df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['Month'] == month]

    if day != 'all':
        df=df[df['Day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    common_month_count = df['Month'].value_counts()[common_month]
    print('Most common month: {}, Count: {}'.format(common_month,common_month_count))

    # display the most common day of week
    common_day = df['Day'].mode()[0]
    common_day_count = df['Day'].value_counts()[common_day]
    print('Most common day: {}, Count: {}'.format(common_day,common_day_count))

    # display the most common start hour
    df['Hour']=df['Start Time'].dt.hour

    common_hour = df['Hour'].mode()[0]
    common_hour_count = df['Hour'].value_counts()[common_hour]
    print('Most common hour: {}, Count: {}'.format(common_hour,common_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    common_start_station_count = df['Start Station'].value_counts()[common_start_station]
    print('Most common Start Station: {}, Count: {}\n'.format(common_start_station,common_start_station_count))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    common_end_station_count = df['End Station'].value_counts()[common_end_station]
    print('Most common End Station: {}, Count: {}\n'.format(common_end_station,common_end_station_count))

    # display most frequent combination of start station and end station trip
    common_trip=df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most common trip: {}\n'.format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('Total travel time: {}\n'.format(total_travel_time))

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print('Average travel time: {}\n'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types=df['User Type'].value_counts()
    print(user_types, end='\n')

    # Display counts of gender if it exists
    if 'Gender' in df.columns:
        gender_count=df['Gender'].value_counts()
        print(gender_count, end='\n')
    else:
        print('The city of Washington doesn\'t have gender data.\n')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        print('Earliest year of birth: {}\n'.format(earliest_year))
        most_recent_year = int(df['Birth Year'].max())
        print('Most recent year of birth: {}\n'.format(most_recent_year))
        most_common_year = int(df['Birth Year'].mode())
        print('Most common year of birth: {}\n'.format(most_common_year))
    else:
        print('The city of Washington doesn\'t have birth year data.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    '''
    Displays five columns of the specified file's data upon request by the user
    Args:
        (str) city - name of the city to analyze
    Returns:
        df - Pandas DataFrame containing raw data by 5 columns at a time
    '''
    raw_data=input('Do you want to view some raw data? Yes or No.\n')
    while raw_data.lower() == 'yes':
        for chunk in pd.read_csv(CITY_DATA[city], chunksize=5):
            print(chunk)
            raw_data=input('Do you want to view some more raw data? Yes or No.\n')
            if raw_data.lower() != 'yes':
                print('Thank you!')
                break
        break

def main():
    while True:
        city, month, day= get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()