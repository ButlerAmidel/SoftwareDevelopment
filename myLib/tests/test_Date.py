# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 20:49:41 2024

@author: ButlerMasango
"""

import unittest
import sys
import os

# Ensure the code directory is in the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

from my_Date import Date

class TestDate(unittest.TestCase):

    def test_initialization_with_string(self):
        date = Date("2024-06-18")
        self.assertEqual(date.year, 2024)
        self.assertEqual(date.month, 6)
        self.assertEqual(date.day, 18)
        
        with self.assertRaises(ValueError):
            Date("2019-12-31")
        
        with self.assertRaises(ValueError):
            Date("2057-01-01")

    def test_initialization_with_tuple(self):
        date = Date(2024, 6, 18)
        self.assertEqual(date.year, 2024)
        self.assertEqual(date.month, 6)
        self.assertEqual(date.day, 18)
        
        with self.assertRaises(ValueError):
            Date(2019, 12, 31)
        
        with self.assertRaises(ValueError):
            Date(2057, 1, 1)

    def test_invalid_initialization(self):
        with self.assertRaises(ValueError):
            Date("invalid-string")
        
        with self.assertRaises(ValueError):
            Date(2024, 6)
        
        with self.assertRaises(ValueError):
            Date(2024)

    def test_isLeapYear(self):
        date = Date("2024-06-18")
        self.assertTrue(date.isLeapYear())
        
        date = Date("2023-06-18")
        self.assertFalse(date.isLeapYear())

    def test_daysInYear(self):
        self.assertEqual(Date.daysInYear(2024), 366)
        self.assertEqual(Date.daysInYear(2023), 365)

if __name__ == '__main__':
    unittest.main()





