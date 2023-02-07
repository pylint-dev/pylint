import datetime
from datetime import datetime

# Make a program to display the various Date Time formats
dateStrings = ["Current date and time: ", "Current year: "]
dateValues = [datetime.datetime.now(), datetime.date.today().strftime("%Y")]

for index in range(len(dateStrings)):
    print(dateStrings[index] + dateValues[index])
