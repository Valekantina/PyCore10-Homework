from datetime import datetime, timedelta
# creating a dictionary with all users names and days of birth
users = [
    {"name": "Bill", "birthday": "13 December 1989"},
    {"name": "John", "birthday": "10 December 1998"},
    {"name": "Kim", "birthday": "15 December 1996"},
    {"name": "Max", "birthday": "16 December 1994"},
    {"name": "Viktor", "birthday": "20 December 1963"},
    {"name": "Valentyna", "birthday": "12 December 1994"},
    {"name": "Dean", "birthday": "09 December 1979"},
]

# defining get_birthdays_per_week function


def get_birthdays_per_week(users):
    # outlining the days of the week as dictionary in day_of_the_week : "name" format
    weekdays = {
        'Monday': '',
        'Tuesday': '',
        'Wednesday': '',
        'Thursday': '',
        'Friday': '',
    }
    # defining the start date of our search (datetime.now)
    # since we need the script to return all birthdays from Saturday of this week until next Friday (including)
    # we will shift the start date depending on the date of running the script
    today = datetime.now().date()
    if today.weekday() == 0:
        start = today + timedelta(days=5)
    if today.weekday() == 1:
        start = today + timedelta(days=4)
    if today.weekday() == 2:
        start = today + timedelta(days=3)
    if today.weekday() == 3:
        start = today + timedelta(days=2)
    if today.weekday() == 4:
        start = today + timedelta(days=1)

    # using for-loop to go through the users dictionary
    for person in users:
        # converting dae of birth from string to datetime format
        # %d - day of the month
        # %B month's name in full
        # %Y year in 4 digits
        birthday = datetime.strptime(person["birthday"], "%d %B %Y")
        dob = datetime(start.year, birthday.month, birthday.day)

        # defining the end date as start date + 7 days forward using timedelta
        end = start + timedelta(days=7)

        # checking if the date of birth (dob) is within range from start date to the end date (today+7 days forward)
        if start <= dob.date() <= end:
            day = dob.weekday()  # if the date is within range - getting the weekday
            if day == 0 or day == 5 or day == 6:
                weekdays['Monday'] += person['name']
                weekdays['Monday'] += ', '
            if day == 1:
                weekdays['Tuesday'] += person['name']
                weekdays['Tuesday'] += ', '
            if day == 2:
                weekdays['Wednesday'] += person['name']
                weekdays['Wednesday'] += ', '
            if day == 3:
                weekdays['Thursday'] += person['name']
                weekdays['Thursday'] += ', '
            if day == 4:
                weekdays['Friday'] += person['name']
                weekdays['Friday'] += ', '
    # using for-loop to go through all items in weekdays dictionary
    for key, value in weekdays.items():
        count = 0
        if len(value) > 0:  # if there is an value in weekdays dictionary - print the result
            print(key + ": " + value[:-2])
        else:
            count += 1
    if count > 0:
        print("There are no more birthdays this week")


# making sure the code will only run when get_bd.py file is executed as a script
if __name__ == '__main__':
    get_birthdays_per_week(users)
