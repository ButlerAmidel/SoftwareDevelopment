# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 20:49:30 2024

@author: ButlerMasango
"""
from enum import Enum
from datetime import datetime, date
from Calendar import Calendar  # Assuming Calendar class is defined in calendar_module
from Date import Date

class DayCountConvention(Enum):
    ACT_365 = 'act/365'
    ACT_360 = 'act/360'
    ACT_ACT = 'act/act'
    THIRTY_360 = '30/360'
    THIRTY_360E = '30/360e'
    THIRTY_360EE = '30/360ee'
    
    @classmethod
    def from_string(cls, basis_str):
        normalized_str = basis_str.strip().lower()
        for basis in cls:
            if basis.value == normalized_str:
                return basis
        raise ValueError(f"Invalid basis: {basis_str}")

class DayCountBasis:
    def __init__(self, basis):
        self.basis = DayCountConvention.from_string(basis)

    def dayCountFraction(self, start_date, end_date):
        """Calculate day count fraction between start_date and end_date based on the specified basis"""
        Calendar.validateDateRange(start_date)
        Calendar.validateDateRange(end_date)
        
        if end_date < start_date:
            raise ValueError("endDate must be greater than or equal to startDate")
        
        #if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
         #   raise ValueError("Both start_date and end_date must be datetime objects")
        
        if self.basis == DayCountConvention.ACT_365:
            return (end_date - start_date).days / 365.0
        
        elif self.basis == DayCountConvention.ACT_360:
            return (end_date - start_date).days / 360.0
        
        elif self.basis == DayCountConvention.ACT_ACT:
            return self.actAct(start_date, end_date)
        
        elif self.basis == DayCountConvention.THIRTY_360:
            return self.thirty360(start_date, end_date)
        
        elif self.basis == DayCountConvention.THIRTY_360E:
            return self.thirty360e(start_date, end_date)
        
        elif self.basis == DayCountConvention.THIRTY_360EE:
            return self.thirty360ee(start_date, end_date)
        
        else:
            raise ValueError("Unsupported basis input")
    
    
    @staticmethod
    def actAct(start_date, end_date):
        """Calculate day count fraction using ACT/ACT basis"""
        
        end_date = Calendar.validateDateRange(start_date, end_date)
        if start_date.year == end_date.year:
            return (end_date - start_date).days / Date.daysInYear(start_date.year)
        else:
            fractionFirstYear = ((date(start_date.year, 12, 31) - start_date).days + 1) / Date.daysInYear(start_date.year)
            fractionLastYear = (end_date - date(end_date.year, 1, 1)).days / Date.daysInYear(end_date.year)
            yearsBetween = (end_date.year - start_date.year - 1)
            return fractionFirstYear + yearsBetween + fractionLastYear
    
    @staticmethod
    def thirty360(start_date, end_date):
        """Calculate day count fraction using 30/360 basis"""
        end_date = Calendar.validateDateRange(start_date, end_date)
        d1, m1, y1 = start_date.day, start_date.month, start_date.year
        d2, m2, y2 = end_date.day, end_date.month, end_date.year
        if d1 == 31:
            d1 = 30
        if d2 == 31 and d1 == 30:
            d2 = 30
        return ((360 * (y2 - y1)) + (30 * (m2 - m1)) + (d2 - d1)) / 360.0
    
    @staticmethod
    def thirty360e(start_date, end_date):
        """Calculate day count fraction using 30/360E basis"""
        end_date = Calendar.validateDateRange(start_date, end_date)
        d1, m1, y1 = start_date.day, start_date.month, start_date.year
        d2, m2, y2 = end_date.day, end_date.month, end_date.year
        if d1 == 31:
            d1 = 30
        if d2 == 31:
            d2 = 30
        return ((360 * (y2 - y1)) + (30 * (m2 - m1)) + (d2 - d1)) / 360.0
    
    @staticmethod
    def thirty360ee(start_date, end_date):
        """Calculate day count fraction using 30/360EE basis"""
        end_date = Calendar.validateDateRange(start_date, end_date)
        d1, m1, y1 = start_date.day, start_date.month, start_date.year
        d2, m2, y2 = end_date.day, end_date.month, end_date.year
        if d1 == 31:
            d1 = 30
        if d2 == 31:
            if d1 < 30:
                d2 = 1
                if m2 == 12:
                    m2 = 1
                    y2 += 1
                else:
                    m2 += 1
            else:
                d2 = 30
        return ((360 * (y2 - y1)) + (30 * (m2 - m1)) + (d2 - d1)) / 360.0






# # Example usage:
# if __name__ == "__main__":
#     basis = 'act/act'
#     day_count_basis = DayCountBasis(basis)
    
#     start_date = date(2024, 6, 1)
#     end_date = date(2024, 12, 31)
    
#     try:
#         fraction = day_count_basis.dayCountFraction(start_date, end_date)
#         print(f"Day count fraction based on {basis}: {fraction}")
#     except ValueError as e:
#         print(f"Error: {str(e)}")

