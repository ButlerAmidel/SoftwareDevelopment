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


class TestInvalidCountryCodes(unittest.TestCase):
    def test_invalidCountryCodes(self):
        # Test with invalid country code
        with self.assertRaises(ValueError) as context:
            Calendar.Calendar("invalidCode")
        self.assertIn("Invalid Country code", str(context.exception))

        # Test with a mix of valid and invalid country codes
        with self.assertRaises(ValueError) as context:
            Calendar.Calendar("ZA+invalidCode")
        self.assertIn("Invalid Country code", str(context.exception))



class TestCalendar(unittest.TestCase):
    
    def setUp(self):
        self.calendar = Calendar.Calendar("za+EG")
    
    def test_isBusinessDay(self):
        # Test regular business day
        business_day = date(2024, 7, 1)  # Monday
        self.assertTrue(self.calendar.isBusinessDay(business_day))

        # Test weekend days
        friday = date(2024,7,6) # Friday..weekend in EG
        saturday = date(2024, 7, 6)  # Saturday
        sunday = date(2024, 7, 7)  # Sunday
        self.assertFalse(self.calendar.isBusinessDay(friday))
        self.assertFalse(self.calendar.isBusinessDay(saturday))
        self.assertFalse(self.calendar.isBusinessDay(sunday))

        # Test public holiday
        public_holiday_eg = date(2024, 7, 7)  # Holiday in EG
        self.assertFalse(self.calendar.isBusinessDay(public_holiday_eg))

        public_holiday_za = date(2024, 6, 30)  # Holiday in za
        self.assertFalse(self.calendar.isBusinessDay(public_holiday_za))

        # Test non-holiday weekday
        non_holiday_weekday = date(2024, 7, 8) 
        self.assertTrue(self.calendar.isBusinessDay(non_holiday_weekday))


    def test_getHolidaysData(self):
            # Test for holidays within a given date range
            start_date = date(2024, 7, 1)
            end_date = date(2024, 7, 31)
            holidays = self.calendar.getHolidaysData(start_date, end_date)
            # one holiday for EG
            self.assertEqual(len(holidays),1)

            # Test for start_date > end_date
            start_date = date(2024, 8, 31)
            end_date = date(2024, 8, 1)
            with self.assertRaises(ValueError):
                self.calendar.getHolidaysData(start_date, end_date)

            # Test for dates out of range
            start_date = date(2019, 12, 31)  # Date before valid range
            end_date = date(2024, 7, 31)
            with self.assertRaises(ValueError):
                self.calendar.getHolidaysData(start_date, end_date)

            start_date = date(2024, 7, 1)
            end_date = date(2057, 1, 1)  # Date after valid range
            with self.assertRaises(ValueError):
                self.calendar.getHolidaysData(start_date, end_date)


    def test_addBusinessDays(self):
        # Test adding 3 business days to a Wednesday
        start_date = date(2024, 7, 3)  # Wednesday
        expected_date = date(2024, 7, 9)  
        self.assertEqual(self.calendar.addBusinessDays(start_date, 3), expected_date)

        # Test adding 5 business days to a Friday with roll forward
        start_date = date(2024, 7, 5)  # Friday
        expected_date = date(2024, 7, 16)  # Next Friday after 5 business days
        self.assertEqual(self.calendar.addBusinessDays(start_date, 5, "f"), expected_date)

        # Test adding -3 business days (subtracting 3 business days) from a Monday
        start_date = date(2024, 7, 15)  # Monday
        expected_date = date(2024, 7, 9)  # Previous Wednesday before 3 business days
        self.assertEqual(self.calendar.addBusinessDays(start_date, -3), expected_date)

        # Test adding 0 business days (no change)
        start_date = date(2024, 7, 1)
        self.assertEqual(self.calendar.addBusinessDays(start_date, 0), start_date)

        # Test adding business days with invalid roll type
        start_date = date(2024, 7, 1)
        with self.assertRaises(ValueError):
            self.calendar.addBusinessDays(start_date, 3, "invalid_roll_type")

        # Test adding business days with roll="mf"
        start_date = date(2024, 6, 28)  # Last business day in July 2024
        expected_date = date(2024, 6, 27)  # Next business day after adding 1 business day
        self.assertEqual(self.calendar.addBusinessDays(start_date, 0, "mf"), expected_date)

        # Test adding business days with roll="mf"
        start_date = date(2024, 6, 1)  # Last business day in July 2024
        expected_date = date(2024, 6, 3)  # Next business day after adding 1 business day
        self.assertEqual(self.calendar.addBusinessDays(start_date, 0, "mp"), expected_date)

    def test_getLastBusinessDateInMonth(self):
        # Test for June 2024 (30th is a Sunday)
        given_date = date(2024, 6, 30)
        last_business_day = self.calendar.getLastBusinessDateInMonth(given_date)
        self.assertEqual(last_business_day, date(2024, 6, 27))  # Last business day in June 2024

        # Test for July 2024 (31st is a Wednesday)
        given_date = date(2024, 7, 15)
        last_business_day = self.calendar.getLastBusinessDateInMonth(given_date)
        self.assertEqual(last_business_day, date(2024, 7, 31))  # Last business day in July 2024

        # Test for February 2024 (29th is a Friday, leap year)
        given_date = date(2024, 2, 15)
        last_business_day = self.calendar.getLastBusinessDateInMonth(given_date)
        self.assertEqual(last_business_day, date(2024, 2, 29))  # Last business day in February 2024

        # Test for February 2023 (28th is a Wednesday, non-leap year)
        given_date = date(2023, 2, 15)
        last_business_day = self.calendar.getLastBusinessDateInMonth(given_date)
        self.assertEqual(last_business_day, date(2023, 2, 28))  # Last business day in February 2023



    def test_numBusinessDaysBetween(self):
        # Test for June 2024 (22 business days)
        start_date = date(2024, 7, 1)
        end_date = date(2024, 7, 31)
        business_days_count = self.calendar.numBusinessDaysBetween(start_date, end_date)
        self.assertEqual(business_days_count, 18)

        # Test for February 2024 (19 business days, leap year)
        start_date = date(2024, 2, 1)
        end_date = date(2024, 2, 29)
        business_days_count = self.calendar.numBusinessDaysBetween(start_date, end_date)
        self.assertEqual(business_days_count, 17)

    def test_addTenor(self):
        # Test adding 1 day
        start_date = date(2024, 6, 27)
        expected_date = date(2024, 7, 1)
        self.assertEqual(self.calendar.addTenor(start_date, "1d", "f", False), expected_date)

        start_date = date(2024, 6, 27)
        expected_date = date(2024, 6, 26)
        self.assertEqual(self.calendar.addTenor(start_date, "-1d", "f", False), expected_date)

        start_date = date(2024, 6, 28)
        expected_date = date(2024, 6, 27)
        self.assertEqual(self.calendar.addTenor(start_date, "1d", "p", False), expected_date)

        # Test adding 2 weeks
        start_date = date(2024, 6, 7)
        expected_date = date(2024, 6, 24)
        self.assertEqual(self.calendar.addTenor(start_date, "2w", "f", False), expected_date)

        # Test adding 2 months
        start_date = date(2024, 6, 15)
        expected_date = date(2024, 8, 15)
        self.assertEqual(self.calendar.addTenor(start_date, "2m", "f", False), expected_date)

        start_date = date(2024, 6, 15)
        expected_date = date(2024, 4, 15)
        self.assertEqual(self.calendar.addTenor(start_date, "-2m", "f", False), expected_date)

        # Test adding 1 year
        start_date = date(2024, 6, 15)
        expected_date = date(2025, 6, 17)
        self.assertEqual(self.calendar.addTenor(start_date, "1y", "f", False), expected_date)

        # Test adding 1 month with preserve month end
        start_date = date(2024, 3, 28)
        expected_date = date(2024, 4, 30)  # February 29, 2024 is the preserved month end
        self.assertEqual(self.calendar.addTenor(start_date, "1m", "f", True), expected_date)

        # Test adding 1 month without preserving month end
        start_date = date(2024, 3, 28)
        expected_date = date(2024, 4, 29)  # Next business day in February
        self.assertEqual(self.calendar.addTenor(start_date, "1m", "f", False), expected_date)


        # Test adding 1 month with 'mf' roll
        start_date = date(2024, 1, 30)
        expected_date = date(2024, 1, 31)  # Assuming February 29 is a business day
        self.assertEqual(self.calendar.addTenor(start_date, "1d", "mf", False), expected_date)

        # Test adding 1 month with 'mp' roll
        start_date = date(2024, 2, 29)
        expected_date = date(2024, 3, 4)  # Previous business day in February
        self.assertEqual(self.calendar.addTenor(start_date, "1d", "mp", False), expected_date)

        # Test invalid roll type
        start_date = date(2024, 6, 15)
        with self.assertRaises(ValueError):
            self.calendar.addTenor(start_date, "1m", "invalid", False)

        # Test invalid tenor format
        start_date = date(2024, 6, 15)
        with self.assertRaises(ValueError):
            self.calendar.addTenor(start_date, "2x", "f", False)



if __name__ == "__main__":
    unittest.main()


