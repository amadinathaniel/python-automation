def days_to_units(num_of_days, conversion_unit):
    if conversion_unit == "hours":
        return f"{num_of_days} days are {num_of_days * 24} hours"
    elif conversion_unit == "minutes":
        return f"{num_of_days} days are {num_of_days * 24 * 60} minutes"
    else:
        return "unsupported unit, Please use 'hours' or 'minutes'"


def validate_and_execute(days_and_units_dictionary):
    try:
        user_input_number = int(days_and_units_dictionary["days"])

        # we want to do conversion only for positive integers
        if user_input_number > 0:
            calculated_value = days_to_units(user_input_number, days_and_units_dictionary["unit"])
            print(calculated_value)
        elif user_input_number == 0:
            print("you entered num 0, please enter a positive value")
        else:
            print("you entered a negative number, no conversion for you")
    except ValueError:
        print("your input is invalid, please enter a number")


user_input_message = "Hey user, enter number of days and conversion unit! \n"
