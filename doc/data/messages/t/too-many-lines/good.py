import datetime
from datetime import datetime

# Make a program to display the various Date Time formats
dateStrings = ["Current date and time: ", "Current year: ", "Month of year: ", "Week number of the year: "]
dateValues = [datetime.datetime.now(), datetime.date.today().strftime("%Y"), datetime.date.today().strftime("%B"), datetime.date.today().strftime("%W")]

for index in range(len(dateStrings)):
    print(dateStrings[index] + dateValues[index])
