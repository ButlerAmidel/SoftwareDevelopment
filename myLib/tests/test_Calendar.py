# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 12:39:03 2024

@author: ButlerMasango
"""

import unittest
from datetime import date, datetime, timedelta
import pandas as pd
import os
import sys

# Adjust the path to import Calendar from Calendar in the code folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

from myLib.code import Calendar  # Assuming your Calendar class is in Calendar module

class TestCalendar(unittest.TestCase):
    
    def setUp(self):
        self.calendar = Calendar.Calendar("za+EG")
    
    def test_isWeekend(self):
        weekend_date = date(2023, 6, 24)  # Saturday
        self.assertTrue(self.calendar.isWeekend(weekend_date))
    
    def test_isBusinessDay(self):
        business_day = date(2023, 6, 26)  # Monday
        self.assertTrue(self.calendar.isBusinessDay(business_day))
    
    def test_getHolidaysData(self):
        start_date = date(2023, 1, 1)
        end_date = date(2023, 12, 31)
        holidays = self.calendar.getHolidaysData(start_date, end_date)
        self.assertEqual(len(holidays), 2)  # Assuming there are 2 holidays in 2023 for "za" and "us"

    def test_addBusinessDays(self):
        start_date = date(2023, 6, 21)  # Wednesday
        expected_date = date(2023, 6, 27)  # Next Wednesday after 3 business days
        self.assertEqual(self.calendar.addBusinessDays(start_date, 3), expected_date)

    def test_getLastBusinessDateInMonth(self):
        given_date = date(2023, 6, 15)  # Any date in June 2023
        last_business_day = self.calendar.getLastBusinessDateInMonth(given_date)
        self.assertEqual(last_business_day, date(2023, 6, 30))  # Last business day in June 2023

    def test_isLastBusinessDayInMonth(self):
        given_date = date(2023, 6, 30)  # Last business day in June 2023
        self.assertTrue(self.calendar.isLastBusinessDayInMonth(given_date))

    def test_addTenor(self):
        start_date = date(2023, 6, 15)
        tenor = "2M"
        roll = "f"
        preserve_month_end = False
        expected_date = date(2023, 8, 15)  # Adding 2 months without preserving month end
        self.assertEqual(self.calendar.addTenor(start_date, tenor, roll, preserve_month_end), expected_date)

    def test_numBusinessDaysBetween(self):
        start_date = date(2023, 6, 1)
        end_date = date(2023, 6, 30)
        business_days_count = self.calendar.numBusinessDaysBetween(start_date, end_date)
        self.assertEqual(business_days_count, 22)  # Assuming there are 22 business days in June 2023

if __name__ == "__main__":
    unittest.main()







'''


import unittest
from datetime import date, datetime, timedelta
import pandas as pd
import os
import sys

# Adjust the path to import Calendar from my_Calendar in the code folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

from my_Calendar import Calendar  # Assuming your Calendar class is in my_Calendar module

class TestCalendar(unittest.TestCase):

    def setUp(self):
        # Initialize Calendar with country codes
        self.calendar = Calendar("US+ZA")

    def test_isBusinessDay_US(self):
        # Test for US holidays
        self.assertTrue(self.calendar.isBusinessDay(date(2024, 7, 4)))  # Independence Day is a holiday in the US

    def test_isBusinessDay_ZA(self):
        # Test for ZA holidays
        self.assertTrue(self.calendar.isBusinessDay(date(2024, 12, 16)))  # Day of Reconciliation is a holiday in South Africa

    def test_addBusinessDays(self):
        # Test adding business days
        start_date = date(2024, 7, 1)  # July 1, 2024 is a business day
        expected_date = date(2024, 7, 5)  # Expected date after adding 3 business days
        self.assertEqual(self.calendar.addBusinessDays(start_date, 3), expected_date)

if __name__ == "__main__":
    unittest.main()

'''


