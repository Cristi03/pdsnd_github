import time
import pandas as pd
import click as click

TIME_DURATION_FOR_EXECUTION = "\nThis took %s seconds."

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

filter_period = ('month', 'day', 'both', 'none')

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')

CONFIRMATION_MESSAGE = "\nPlease confirm the option\'s you selected. \n\n City(ies): {}\n Month(s): {}\n Weekday(s): {}\n\n [" \
                       "Confirmation] -> Yes\n [Decline] -> No\n\n>"

START_TIME = 'Start Time'
START_STATION = 'Start Station'
TRIP_DURATION = 'Trip Duration'
END_STATION = 'End Station'
BIRTH_YEAR = 'Birth Year'

def get_user_options(prompt, options=('yes', 'no')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        option = input(prompt).lower().strip()
        # kill the program if the user chose to do this
        if option == 'q':
            print('You just exited the program. Thank you!!')
            raise SystemExit
        # triggers if the input has only one name
        elif ',' not in option:
            if option in options:
                break
        # triggers if the input has more than one name
        elif ',' in option:
            option = [i.strip().lower() for i in option.split(',')]
            if list(filter(lambda x: x in options, option)) == option:
                break

        prompt = "\nSomething is not right, please insert again your option: \n>"

    return option


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global confirmation, month, day

    print('Hello! Let\'s explore some US bikeshare data!')
    print("If you want to exit the program please press 'q'!!")
    print("During the program multiple menu options will be shown. Important for the ones with format '_x_' only the number is relevant!!")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = get_user_options("\nWould you like to see data for Chicago, New York, or Washington?\n>", CITY_DATA.keys())

        filter_p = get_user_options("\nWould you like to filter the data by month, day, both, or none at all?\n>", filter_period)

        time_filter_definition(city, filter_p)

        if confirmation == 'yes':
            break
        else:
            print("\nLet's try this again!")
    print('-' * 40)

    return city, month, day


def time_filter_definition(city, filter_p):
    global confirmation
    if filter_p.__eq__('month'):
        # get user input for month (all, january, february, ... , june)
        filter_by_month(city)

    elif filter_p.__eq__('day'):
        # get user input for day of week (all, monday, tuesday, ... sunday)
        filter_by_day(city)

    elif filter_p.__eq__('both'):
        filter_by_day_and_month(city)

    elif filter_p.__eq__('none'):
        print("No filter applied!!")

        confirmation = get_user_options(CONFIRMATION_MESSAGE
                                        .format(city, None, None))


def filter_by_day_and_month(city):
    global day, month, confirmation
    day = get_user_options("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n>", weekdays)
    month = get_user_options("\nWhich month - January, February, March, April, May, or June\n>",
                             months)
    confirmation = get_user_options(CONFIRMATION_MESSAGE
                                    .format(city, month, day))


def filter_by_day(city):
    global day, confirmation, month
    day = get_user_options("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n>", weekdays)
    month = ""
    confirmation = get_user_options(CONFIRMATION_MESSAGE
                                    .format(city, month, day))


def filter_by_month(city):
    global month, confirmation, day
    month = get_user_options("\nWhich month - January, February, March, April, May, or June\n>",
                             months)
    day = ""
    confirmation = get_user_options(CONFIRMATION_MESSAGE
                                    .format(city, month, day))


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
    print('Start loading data\'s!')

    start_time = time.time()

    # filter the data according to the selected city filters
    if isinstance(city, list):
        df = pd.concat(map(lambda city_lambda: pd.read_csv(CITY_DATA[city_lambda]), city),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', START_TIME, 'End Time',
                                     TRIP_DURATION, START_STATION,
                                     END_STATION, 'User Type', 'Gender',
                                     BIRTH_YEAR])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # create columns to display statistics
    df[START_TIME] = pd.to_datetime(df[START_TIME])
    df['Month'] = df[START_TIME].dt.month
    df['Weekday'] = df[START_TIME].dt.day_name()
    df['Start Hour'] = df[START_TIME].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month_lambda: df[df['Month'] ==
                                                   (months.index(month_lambda) + 1)], month))
    else:
        if month == "":
            print("No Month selected")
        else:
            df = df[df['Month'] == (months.index(month) + 1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==
                                          (day.title())], day))
    else:
        if day == "":
            print("No Day selected")
        else:
            df = df[df['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-' * 40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print('The month with the most travels is: ' +
          str(months[most_common_month - 1]).title() + '.')

    # display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('The most common day of the week is: ' +
          str(most_common_day) + '.')
    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' +
          str(most_common_hour) + '.')

    print(TIME_DURATION_FOR_EXECUTION % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df[START_STATION].mode()[0])
    print("The most common start station is: " +
          most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df[END_STATION].mode()[0])
    print("The most common start end is: " +
          most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['Start-End Combination'] = (df[START_STATION] + ' - ' +
                                   df[END_STATION])
    most_common_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("The most common start-end combination "
          "of stations is: " + most_common_start_end_combination)

    print(TIME_DURATION_FOR_EXECUTION % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_param = df[TRIP_DURATION].sum()
    total_travel_time_param = (str(int(total_travel_time_param // 86400)) +
                               'd ' +
                               str(int((total_travel_time_param % 86400) // 3600)) +
                               'h ' +
                               str(int(((total_travel_time_param % 86400) % 3600) // 60)) +
                               'm ' +
                               str(int(((total_travel_time_param % 86400) % 3600) % 60)) +
                               's')
    print('The total travel time is : ' +
          total_travel_time_param + '.')

    # display mean travel time
    mean_travel_time = df[TRIP_DURATION].mean()
    mean_travel_time = (str(int(mean_travel_time // 60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("The mean travel time is : " +
          mean_travel_time + ".")

    print(TIME_DURATION_FOR_EXECUTION % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("User types distribution:")
    print(user_types)
    # Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender_distribution)
    except KeyError:
        print("We're sorry! There is no data of user genders for {}."
              .format(city.title()))

        # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df[BIRTH_YEAR].min()))
        print("\nThe oldest person to ride one bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df[BIRTH_YEAR].max()))
        print("The youngest person to ride one bike was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(df[BIRTH_YEAR].mode()[0]))
        print("The most common birth year amongst riders is: " + most_common_birth_year)
    except:
        print("There is no data of birth year for {}. We're sorry!".format(city.title()))

    print(TIME_DURATION_FOR_EXECUTION % (time.time() - start_time))
    print('-' * 40)


def raw_data(df, mark_place):
    """Display 5 line of sorted raw data each time."""

    print("\nYou chose to see raw data.")

    # this variable holds where the user last stopped
    if mark_place > 0:
        last_place = get_user_options("\nWould you like to continue from where left last time? \n [y] Yes\n [n] No\n\n>")
        if last_place == 'n':
            mark_place = 0

    # sort data by column
    if mark_place == 0:
        sort_df = get_user_options("\nHow would you like to sort the way the data is "
                                   "displayed in the dataframe? Hit Enter to view "
                                   "unsorted.\n \n [_1_] Start Time\n [_2_] End Time\n "
                                   "[_3_] Trip Duration\n [_4_] Start Station\n "
                                   "[_5_] End Station\n\n>",
                                   ('1', '2', '3', '4', '5', ''))

        df = sort_menu(df, sort_df)

    # each loop displays 5 lines of raw data
    mark_place = keep_printing_data(df, mark_place)

    return mark_place


def keep_printing_data(df, mark_place):
    while True:
        for i in range(mark_place, len(df.index)):
            print("\n")
            print(df.iloc[mark_place:mark_place + 5].to_string())
            print("\n")
            mark_place += 5

            if get_user_options("Do you want to keep printing data?"
                                "\n\n[yes]Yes\n[no]No\n\n>") == 'yes':
                continue
            else:
                break
        break
    return mark_place


def sort_menu(df, sort_df):
    asc_or_desc = get_user_options("\nDo you like want to sort the data ascending or "
                                   "descending? \n [a] Ascending\n [d] Descending"
                                   "\n\n>",
                                   ('a', 'd'))
    if asc_or_desc == 'a':
        asc_or_desc = True
    elif asc_or_desc == 'd':
        asc_or_desc = False
    if sort_df == '1':
        df = df.sort_values([START_TIME], ascending=asc_or_desc)
    elif sort_df == '2':
        df = df.sort_values(['End Time'], ascending=asc_or_desc)
    elif sort_df == '3':
        df = df.sort_values([TRIP_DURATION], ascending=asc_or_desc)
    elif sort_df == '4':
        df = df.sort_values([START_STATION], ascending=asc_or_desc)
    elif sort_df == '5':
        df = df.sort_values([END_STATION], ascending=asc_or_desc)
    elif sort_df == '':
        pass
    return df


def main_menu_options(city, df, mark_place):
    while True:
        select_data = get_user_options("\nPlease select the information you whant to see "
                                       "\n\n [_1_] Time Stats\n [_2_] "
                                       "Station Stats\n [_3_] Trip Duration Stats\n "
                                       "[_4_] User Stats\n [_5_] Display Raw Data\n "
                                       "[_r_] Restart\n [_q_] Quit\n\n>",
                                       ('1', '2', '3', '4', '5', 'r', 'q'))
        click.clear()
        if select_data == '1':
            time_stats(df)
        elif select_data == '2':
            station_stats(df)
        elif select_data == '3':
            trip_duration_stats(df)
        elif select_data == '4':
            user_stats(df, city)
        elif select_data == '5':
            mark_place = raw_data(df, mark_place)
        elif select_data == 'r':
            break
        elif select_data == 'q':
            print('You quit the program. Thank you!!')
            raise SystemExit


def main():
    while True:
        city, month_main, day_main = get_filters()
        df = load_data(city, month_main, day_main)

        mark_place = 0
        main_menu_options(city, df, mark_place)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
