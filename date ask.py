import datetime

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


start_date = input("Please enter the start date of your experiment in 'YYYY-MM-DD' format: ")

while validate(start_date) == False:
    start_date = input("Invalid date. Please try again in 'YYYY-MM-DD' format: ")

end_date = input("please enter the End Date of your experiment in 'YYYY-MM-DD' format: ")

while validate(end_date) == False:
    start_date = input("Invalid date. Please try again in 'YYYY-MM-DD' format: ")