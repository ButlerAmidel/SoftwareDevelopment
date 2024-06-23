# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:16:36 2024

@author: ButlerMasango
"""

# date.py
from datetime import date, datetime  # Import necessary modules

class Date(date):  # Define Date class inheriting from datetime.date
    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):  # Check if input is a string
            dt = datetime.strptime(args[0], "%Y-%m-%d")  # Parse string to datetime object
            # Validate date range (2020-01-01 to 2056-12-31)
            if not (date(2020, 1, 1) <= dt.date() <= date(2056, 12, 31)):
                raise ValueError("Date must be between 2020-01-01 and 2056-12-31.")
            # Create a new instance of Date with year, month, and day from dt
            return super(Date, cls).__new__(cls, dt.year, dt.month, dt.day)
        
        elif len(args) == 3:  # Check if input is a tuple of (year, month, day)
            dt = date(args[0], args[1], args[2])  # Create a datetime.date object
            # Validate date range (2020-01-01 to 2056-12-31)
            if not (date(2020, 1, 1) <= dt <= date(2056, 12, 31)):
                raise ValueError("Date must be between 2020-01-01 and 2056-12-31.")
            # Create a new instance of Date with year, month, and day from args
            return super(Date, cls).__new__(cls, *args)
        
        else:
            raise ValueError("Invalid arguments. Use 'YYYY-MM-DD' or (YYYY, MM, DD)")

    def isLeapYear(self):  # Instance method to check if the year is a leap year
        """Check if the year is a leap year using standard leap year rules."""
        year = self.year
        return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)

    def daysInYear(self):  # Instance method to calculate days in the instantiated year
        """Calculate the number of days in the instantiated year using the isLeapYear method."""
        return 366 if self.isLeapYear() else 365

# Example usage:

new_date = Date(2023,1,1)
print(new_date.daysInYear())




