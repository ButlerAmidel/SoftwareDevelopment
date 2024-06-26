# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 21:10:57 2024

@author: ButlerMasango
"""
import unittest
import sys
import os

# Ensure the code directory is in the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

# Now you can import your module
from Rate import Rate, CompoundingFrequency, DayCountConvention

'''

class TestEquivalentRate(unittest.TestCase):

    def test_equivalentRate(self):
        # Test case 1: Annual compounding, ACT/360
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACA, DayCountConvention.ACT_360,
                                          CompoundingFrequency.NACA, DayCountConvention.ACT_360)
        self.assertAlmostEqual(rate, 0.05, places=10)

        # Test case 2: Annual to semi-annual compounding
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACA, DayCountConvention.ACT_360,
                                          CompoundingFrequency.NACS, DayCountConvention.ACT_360)
        self.assertAlmostEqual(rate, 0.04902502420663182, places=10)

        # Test case 3: Semi-annual to monthly compounding
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACS, DayCountConvention.ACT_360,
                                          CompoundingFrequency.NACM, DayCountConvention.ACT_360)
        self.assertAlmostEqual(rate, 0.04879127741515413, places=10)

        # Test case 4: Monthly to continuous compounding
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACM, DayCountConvention.ACT_360,
                                          CompoundingFrequency.NACC, DayCountConvention.ACT_360)
        self.assertAlmostEqual(rate, 0.04883667642301993, places=10)

        # Test case 5: Daily to annual compounding
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACD, DayCountConvention.ACT_360,
                                          CompoundingFrequency.NACA, DayCountConvention.ACT_360)
        self.assertAlmostEqual(rate, 0.05001327456738463, places=10)

        # Test case 6: Different day count conventions (ACT/365)
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACA, DayCountConvention.ACT_360,
                                          CompoundingFrequency.NACA, DayCountConvention.ACT_365)
        self.assertAlmostEqual(rate, 0.049317073170731705, places=10)

        # Test case 7: Annual compounding, ACT/365 to ACT/360
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACA, DayCountConvention.ACT_365,
                                          CompoundingFrequency.NACA, DayCountConvention.ACT_360)
        self.assertAlmostEqual(rate, 0.05068493150684931, places=10)

        # Test case 8: Semi-annual compounding, ACT/365 to monthly compounding, ACT/360
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACS, DayCountConvention.ACT_365,
                                          CompoundingFrequency.NACM, DayCountConvention.ACT_360)
        self.assertAlmostEqual(rate, 0.04894747009970785, places=10)

        # Test case 9: Weekly compounding, ACT/365 to continuous compounding, ACT/360
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACW, DayCountConvention.ACT_365,
                                          CompoundingFrequency.NACC, DayCountConvention.ACT_360)
        self.assertAlmostEqual(rate, 0.04897001763668472, places=10)

        # Test case 10: Continuous compounding, ACT/365 to daily compounding, ACT/360
        rate = Rate.equivalentRate(0.05, CompoundingFrequency.NACC, DayCountConvention.ACT_365,
                                          CompoundingFrequency.NACD, DayCountConvention.ACT_360)
        self.assertAlmostEqual(rate, 0.05003471448354188, places=10)

    def test_invalidInputs(self):
        # Test with invalid compounding frequency
        with self.assertRaises(ValueError):
            Rate.equivalentRate(0.05, 'invalid_compounding', DayCountConvention.ACT_360,
                                       CompoundingFrequency.NACA, DayCountConvention.ACT_360)

        # Test with invalid day count convention
        with self.assertRaises(ValueError):
            Rate.equivalentRate(0.05, CompoundingFrequency.NACA, 'invalid_day_count',
                                       CompoundingFrequency.NACA, DayCountConvention.ACT_360)

'''

class TestDiscountFactor(unittest.TestCase):

    def test_discountFactor(self):
        from datetime import date

        # Test case 1: Annual compounding, ACT/360
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACA, DayCountConvention.ACT_360,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951229424500714, places=10)

        # Test case 2: Semi-annual compounding, ACT/360
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACS, DayCountConvention.ACT_360,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951814396476418, places=10)

        # Test case 3: Monthly compounding, ACT/360
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACM, DayCountConvention.ACT_360,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951969721710457, places=10)

        # Test case 4: Continuous compounding, ACT/360
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACC, DayCountConvention.ACT_360,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951229424500714, places=10)

        # Test case 5: Daily compounding, ACT/360
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACD, DayCountConvention.ACT_360,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951230271715037, places=10)

        # Test case 6: Annual compounding, ACT/365
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACA, DayCountConvention.ACT_365,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951229424500714, places=10)

        # Test case 7: Semi-annual compounding, ACT/365
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACS, DayCountConvention.ACT_365,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951814396476418, places=10)

        # Test case 8: Monthly compounding, ACT/365
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACM, DayCountConvention.ACT_365,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951969721710457, places=10)

        # Test case 9: Continuous compounding, ACT/365
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACC, DayCountConvention.ACT_365,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951229424500714, places=10)

        # Test case 10: Daily compounding, ACT/365
        df = Rate.discountFactor(0.05, CompoundingFrequency.NACD, DayCountConvention.ACT_365,
                                        date(2023, 1, 1), date(2024, 1, 1))
        self.assertAlmostEqual(df, 0.951230271715037, places=10)



    
    def test_invalidInputsDiscountFactor(self):
        from datetime import date

        # Test with invalid compounding frequency
        with self.assertRaises(ValueError):
            Rate.discountFactor(0.05, 'invalid_compounding', DayCountConvention.ACT_360,
                                       date(2023, 1, 1), date(2024, 1, 1))

        # Test with invalid day count convention
        with self.assertRaises(ValueError):
            Rate.discountFactor(0.05, CompoundingFrequency.NACA, 'invalid_day_count',
                                       date(2023, 1, 1), date(2024, 1, 1))





if __name__ == '__main__':
    unittest.main()







