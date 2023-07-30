# The below function doesn't work correctly. It should sum all the numbers at the
# current time. For example, 01:02:03 should return 6. Improve and fix the function,
# and write unit test(s) for it. Use any testing framework you're familiar with.


# [TODO]: fix the function
def sum_current_time(time_str: str) -> int:
    """Expects data in the format HH:MM:SS"""
    if not isinstance(time_str, str):
        raise TypeError("This is not a string")
    list_of_nums = time_str.split(":")
    list_of_ints = []
    for number in list_of_nums:
        if number.isdigit() == True:
            list_of_ints.append(int(number))
        else:
            raise ValueError("The date must be numbers")
    hours = list_of_ints[0]
    minutes = list_of_ints[1]
    seconds = list_of_ints[2]
    if hours > 24 or hours < 0:
        raise ValueError("This is not a valid number of hours")
    if minutes > 60 or hours < 0:
        raise ValueError("This is not a valid number of minutes")
    if seconds > 60 or seconds < 0:
        raise ValueError("This is not a valid number of seconds")
    return sum(list_of_ints)


print(sum_current_time("01:02:03"))
