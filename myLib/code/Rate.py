# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:47:20 2024

@author: ButlerMasango
"""

import math
import enum

class CompoundingFrequency(enum.Enum):
    NACA = 1  # Annual compounding
    NACS = 2  # Semi-annual compounding
    NACM = 12  # Monthly compounding
    NACW = 52  # Weekly compounding
    NACD = 365  # Daily compounding
    NACC = 0  # Continuous compounding

    @classmethod
    def getPeriodsPerYear(cls, compounding):
        if not isinstance(compounding, cls):
            raise ValueError(f"Invalid compounding frequency: {compounding}")
        if compounding == cls.NACC:
            return math.inf
        return compounding.value


class DayCountConvention(enum.Enum):
    ACT_360 = 'act/360'
    ACT_365 = 'act/365'
    
    @classmethod
    def from_string(cls, basis_str):
        normalized_str = basis_str.strip().lower()
        for basis in cls:
            if basis.value == normalized_str:
                return basis
        raise ValueError(f"Invalid basis: {basis_str}")



class Rate:
    
    @staticmethod
    def equivalentRate(rate, fromCompounding, fromBasis, toCompounding, toBasis):
        
        fromPeriodsPerYear = CompoundingFrequency.getPeriodsPerYear(fromCompounding)
        toPeriodsPerYear = CompoundingFrequency.getPeriodsPerYear(toCompounding)

        if fromBasis == DayCountConvention.ACT_360:
            fromBasisDays = 360.0
        elif fromBasis == DayCountConvention.ACT_365:
            fromBasisDays = 365.0
        else:
            raise ValueError("Unsupported fromBasis")

        if toBasis == DayCountConvention.ACT_360:
            toBasisDays = 360.0
        elif toBasis == DayCountConvention.ACT_365:
            toBasisDays = 365.0
        else:
            raise ValueError("Unsupported toBasis")

        dem = fromBasisDays * toPeriodsPerYear
        num = fromPeriodsPerYear * toBasisDays

        if fromCompounding == CompoundingFrequency.NACC:
            if toCompounding == CompoundingFrequency.NACC:
                return rate * (fromBasisDays / toBasisDays)
            else:
                return (math.exp(rate * toBasisDays / dem) - 1) * toPeriodsPerYear
        elif toCompounding == CompoundingFrequency.NACC:
            return fromPeriodsPerYear * math.log(1 + rate / fromPeriodsPerYear) * toBasisDays / fromBasisDays
        else:
            return (((1 + rate / fromPeriodsPerYear) ** (num / dem)) - 1) * toPeriodsPerYear

    @staticmethod
    def discountFactor(rate, compounding, dayCountConvention, startDate, endDate):
        delta_days = (endDate - startDate).days

        if dayCountConvention == DayCountConvention.ACT_360:
            day_count_factor = delta_days / 360.0
        elif dayCountConvention == DayCountConvention.ACT_365:
            day_count_factor = delta_days / 365.0
        else:
            raise ValueError("Unsupported day count convention")

        if compounding == CompoundingFrequency.NACC:
            return math.exp(-rate * day_count_factor)
        else:
            periods_per_year = CompoundingFrequency.getPeriodsPerYear(compounding)
            return (1 + rate / periods_per_year) ** (-periods_per_year * day_count_factor)





# from datetime import date

# # Example usage of the RateUtility class
# rate = 0.10  # 10% rate

# # Convert from NACA with ACT/365 to NACM with ACT/360
# converted_rate = Rate.equivalentRate(
#     rate=rate,
#     fromCompounding=CompoundingFrequency.NACC,
#     fromBasis=DayCountConvention.ACT_365,
#     toCompounding=CompoundingFrequency.NACM,
#     toBasis=DayCountConvention.ACT_360
# )

# print(f"Converted rate: {converted_rate:.6f}")

# # Calculate discount factor
# start_date = date(2023, 1, 1)
# end_date = date(2024, 1, 1)
# discount_factor = Rate.discountFactor(
#     rate=rate,
#     compounding=CompoundingFrequency.NACC,
#     dayCountConvention=DayCountConvention.ACT_365,
#     startDate=start_date,
#     endDate=end_date
# )

# print(f"Discount factor: {discount_factor:.6f}")

