# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 23:21:12 2024

@author: ButlerMasango
"""

import unittest
import sys
import os
from datetime import date

# Ensure the code directory is in the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

from my_DayCountBasis import DayCountBasis, DayCountConvention
#from myCalendar import Calendar

class TestDayCountBasis(unittest.TestCase):

    def test_act_365(self):
        dcb = DayCountBasis('act/365')
        start_date = date(2023, 1, 1)
        end_date = date(2024, 1, 1)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 1.0, places=10)
        
        start_date = date(2023, 2, 1)
        end_date = date(2023, 8, 1)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 0.5, places=10)

    def test_act_360(self):
        dcb = DayCountBasis('act/360')
        start_date = date(2023, 1, 1)
        end_date = date(2024, 1, 1)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 1.0138888888888888, places=10)

        start_date = date(2023, 2, 1)
        end_date = date(2023, 8, 1)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 0.5055555555555555, places=10)

    def test_act_act(self):
        dcb = DayCountBasis('act/act')
        start_date = date(2023, 1, 1)
        end_date = date(2024, 1, 1)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 1.0, places=10)
        
        start_date = date(2023, 2, 1)
        end_date = date(2023, 8, 1)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 0.5, places=10)

    def test_thirty_360(self):
        dcb = DayCountBasis('30/360')
        start_date = date(2023, 1, 30)
        end_date = date(2023, 8, 30)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 7/12, places=10)
        
        start_date = date(2023, 2, 28)
        end_date = date(2024, 2, 28)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 1.0, places=10)

    def test_thirty_360e(self):
        dcb = DayCountBasis('30/360e')
        start_date = date(2023, 1, 30)
        end_date = date(2023, 8, 30)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 7/12, places=10)
        
        start_date = date(2023, 2, 28)
        end_date = date(2024, 2, 28)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 1.0, places=10)

    def test_thirty_360ee(self):
        dcb = DayCountBasis('30/360ee')
        start_date = date(2023, 1, 30)
        end_date = date(2023, 8, 30)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 7/12, places=10)
        
        start_date = date(2023, 2, 28)
        end_date = date(2024, 2, 28)
        fraction = dcb.dayCountFraction(start_date, end_date)
        self.assertAlmostEqual(fraction, 1.0, places=10)

    def test_invalid_basis(self):
        with self.assertRaises(ValueError):
            DayCountBasis('invalid_basis')

    def test_end_date_before_start_date(self):
        dcb = DayCountBasis('act/365')
        start_date = date(2024, 1, 1)
        end_date = date(2023, 1, 1)
        with self.assertRaises(ValueError):
            dcb.dayCountFraction(start_date, end_date)

if __name__ == '__main__':
    unittest.main()
