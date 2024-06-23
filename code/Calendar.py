import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
#import calendar

class Calendar:
    retrievalDatetime = None
    availableCountries = None 
    validDateRange = (date(2020, 1, 1), date(2056, 12, 31))  # Valid date range

    def __init__(self, countryCode):
        self.countryCodes = [code.upper() for code in countryCode.split("+")]
        self.holidayData = self.loadHoliday("nager_public_holidays.csv", self.countryCodes)
        self.weekendTypes = self.loadWeekend("country_weekend_types.csv")
    
    @classmethod
    def loadHoliday(cls, path, countryCodes):
        """Load holiday data from CSV"""
        holidaysDf = pd.read_csv(path)
        holidaysDf["date"] = pd.to_datetime(holidaysDf['date']).dt.date
        
        # Validate country codes
        cls.validateCountryCode(cls.availableCountries, holidaysDf, countryCodes)
        
        # Filter holidays for specified country codes
        holidaysDf = holidaysDf[holidaysDf['countryCode'].isin(countryCodes)]
        
        Calendar.retrievalDatetime = pd.to_datetime(holidaysDf['extraction_date']).iloc[0]
        
        return holidaysDf[['date', 'name', 'countryCode']]

    
    @classmethod
    def loadWeekend(cls, path):
        """Load weekend data from CSV"""
        weekendData = pd.read_csv(path)
        weekendMapping = {
            "Saturday-Sunday": (5, 6),
            "Friday-Saturday": (4, 5),
            "Thursday-Friday": (3, 4)
        }

        # Map weekend types to country codes
        countryWeekends = {}
        for _, row in weekendData.iterrows():
            countryCode = row["Country Code"]
            weekendType = row["Weekend Type"]
            if weekendType in weekendMapping:
                countryWeekends[countryCode] = weekendMapping[weekendType]
            else:
                raise ValueError(f"Unknown weekend type: {weekendType}")
        
        return countryWeekends
        
    @classmethod
    def validateCountryCode(cls, availableCountries, holidaysDf, countryCodes):
        """Validate if country codes are in the available country list"""
        availableCountries = set(holidaysDf["countryCode"].unique())
        invalidCountryCodes = [cc for cc in countryCodes if cc not in availableCountries]
        if invalidCountryCodes:
            raise ValueError("Invalid Country code ", invalidCountryCodes)
        return countryCodes

    @staticmethod
    def validateDateRange(startDate, endDate=None):
        """Validate if given dates are within the valid range and that startDate is before endDate"""
        startRange, endRange = Calendar.validDateRange
        
        if not (startRange <= startDate <= endRange):
            raise ValueError(f"Start date {startDate} is out of the valid range: {startRange} to {endRange}")
        
        if endDate:
            if not (startRange <= endDate <= endRange):
                raise ValueError(f"End date {endDate} is out of the valid range: {startRange} to {endRange}")
            if startDate > endDate:
                raise ValueError("Start date must be before end date")
        else:
            endDate = endRange
        
        return endDate
    
    def isWeekend(self, givenDate):
        """Check if a given date is a weekend"""
        self.validateDateRange(givenDate)
        for country in self.countryCodes:
            if country in self.weekendTypes:
                if givenDate.weekday() in self.weekendTypes[country]:
                    return True
            else:
                raise ValueError(f"Weekend information not available for country code: {country}")
        return False
    
    def isBusinessDay(self, givenDate):
        """Check if a given date is a business day"""
        self.validateDateRange(givenDate)
        if self.isWeekend(givenDate):
            return False
        for code in self.countryCodes:
            if givenDate in self.holidayData['date'].values:
                return False
        return True   

    def getHolidaysData(self, startDate, endDate=None):
        """Retrieve holidays between two dates"""
        endDate = self.validateDateRange(startDate, endDate)
        filteredHolidays = self.holidayData[
            (self.holidayData["date"] >= startDate) &
            (self.holidayData["date"] <= endDate)
        ]
        return filteredHolidays

    def addBusinessDays(self, startDate, numBusinessDays, startDateRoll=None):
        """Add a specified number of business days to a start date"""
        self.validateDateRange(startDate)
    
        # Validate startDateRoll
        validRolls = {"f", "p", "mf", "mp", None}
        if startDateRoll is not None and startDateRoll.lower() not in validRolls:
            raise ValueError(f"Invalid roll type: '{startDateRoll}'. Expected 'f', 'p', 'mf', 'mp', or None.")
    
        # Adjust startDate according to startDateRoll if startDateRoll is specified
        if startDateRoll is not None:
            roll = startDateRoll.lower()
            if roll == "f":
                while not self.isBusinessDay(startDate):
                    startDate += timedelta(days=1)
            elif roll == "p":
                while not self.isBusinessDay(startDate):
                    startDate -= timedelta(days=1)
            elif roll == "mf":
                nextBusinessDay = startDate + timedelta(days=1)
                while not self.isBusinessDay(nextBusinessDay):
                    nextBusinessDay += timedelta(days=1)
                if nextBusinessDay.month != startDate.month:
                    while not self.isBusinessDay(startDate):
                        startDate -= timedelta(days=1)
            elif roll == "mp":
                previousBusinessDay = startDate - timedelta(days=1)
                while not self.isBusinessDay(previousBusinessDay):
                    previousBusinessDay -= timedelta(days=1)
                if previousBusinessDay.month != startDate.month:
                    while not self.isBusinessDay(startDate):
                        startDate += timedelta(days=1)
    
        # If numBusinessDays is 0 and startDateRoll is None, return startDate
        if numBusinessDays == 0 and startDateRoll is None:
            return startDate
    
        # Initialize currentDate based on adjusted startDate
        currentDate = startDate
        businessDaysAdded = 0
    
        # Add or subtract days until the required number of business days are added/subtracted
        if numBusinessDays > 0:
            while businessDaysAdded < numBusinessDays:
                currentDate += timedelta(days=1)
                if self.isBusinessDay(currentDate):
                    businessDaysAdded += 1
        elif numBusinessDays < 0:
            while businessDaysAdded > numBusinessDays:
                currentDate -= timedelta(days=1)
                if self.isBusinessDay(currentDate):
                    businessDaysAdded -= 1
    
        return currentDate


 
    def getLastBusinessDateInMonth(self, givenDate):
        """Find the last business day in a given month"""
        self.validateDateRange(givenDate)
        
        # Manually calculate the last date of the month
        if givenDate.month == 12:
            lastDate = date(givenDate.year + 1, 1, 1) - timedelta(days=1)
        else:
            lastDate = date(givenDate.year, givenDate.month + 1, 1) - timedelta(days=1)
        
        # Iterate backwards to find the last business day
        while not self.isBusinessDay(lastDate):
            lastDate -= timedelta(days=1)
    
        return lastDate

    
    def isLastBusinessDayInMonth(self, givenDate):
        """Check if a given date is the last business day of the month"""
        self.validateDateRange(givenDate)
        return self.getLastBusinessDateInMonth(givenDate) == givenDate

    def addTenor(self, startDate, tenor, roll, preserveMonthEnd):
        """Add a specified tenor to the start date"""
        tenor = tenor.lower()
        if not isinstance(startDate, date):
            raise ValueError("The 'startDate' must be a datetime.date object.")
        validRolls = {"f", "p", "mf", "mp"}
        roll = roll.lower()
        if roll not in validRolls:
            raise ValueError(f"Invalid roll type: '{roll}'. Expected 'f', 'p', 'mf', or 'mp'.")
        if isinstance(preserveMonthEnd, str):
            preserveMonthEnd = preserveMonthEnd.strip().lower() == "true"
        elif not isinstance(preserveMonthEnd, bool):
            raise ValueError("The 'preserveMonthEnd' parameter must be 'True' or 'False'.")
        unit = tenor[-1]
        amount = int(tenor[:-1])
        if unit == "d":
            rawEndDate = startDate + timedelta(days=amount)
        elif unit == "w":
            rawEndDate = startDate + timedelta(weeks=amount)
        elif unit == "m":
            rawEndDate = startDate + relativedelta(months=amount)
        elif unit == "y":
            rawEndDate = startDate + relativedelta(years=amount)
        else:
            raise ValueError(f"Invalid tenor unit: '{unit}'. Expected 'd', 'w', 'm', or 'y'.")
        if preserveMonthEnd and (unit in ("m", "y")) and self.isLastBusinessDayInMonth(startDate):
            rawEndDate = self.getLastBusinessDateInMonth(rawEndDate)
        if self.isBusinessDay(rawEndDate):
            finalEndDate = rawEndDate
        else:
            if roll == "f":
                finalEndDate = self.addBusinessDays(rawEndDate, 1)
            elif roll == "p":
                while not self.isBusinessDay(rawEndDate):
                    rawEndDate -= timedelta(days=1)
                finalEndDate = rawEndDate
            elif roll == "mf":
                finalEndDate = self.addBusinessDays(rawEndDate, 1)
                if finalEndDate.month != rawEndDate.month:
                    finalEndDate -= timedelta(days=1)
                    while not self.isBusinessDay(finalEndDate):
                        finalEndDate -= timedelta(days=1)
            elif roll == "mp":
                finalEndDate = rawEndDate
                while not self.isBusinessDay(rawEndDate):
                    finalEndDate = rawEndDate
                    rawEndDate -= timedelta(days=1)
                if finalEndDate.month != rawEndDate.month:
                    finalEndDate = self.addBusinessDays(finalEndDate + timedelta(days=1), 0)
        self.validateDateRange(finalEndDate)
        return finalEndDate

    def numBusinessDaysBetween(self, startDate, endDate):
        """Calculate the number of business days between two dates"""
        endDate = self.validateDateRange(startDate, endDate)
        currentDate = startDate
        businessDaysCount = 0
        
        while currentDate <= endDate:
            if self.isBusinessDay(currentDate):
                businessDaysCount += 1
            currentDate += timedelta(days=1)
        
        return businessDaysCount
    
    
    

zaCal = Calendar("za")

#print(zaCal.getHolidaysData(date(2024,1,1), date(2024,12,31)))


#print(zaCal.isBusinessDay(date(2024,6,24)))


#print(zaCal.numBusinessDaysBetween(date(2024,1,1), date(2024,12,31)))


#print(zaCal.getHolidaysData(date(2024,1,1), date(2024,12,31)))

#print(zaCal.getLastBusinessDateInMonth(date(2024,6,2)))

#print(zaCal.addBusinessDays(date(2024,6,1),0,"mp"))

#print(zaCal.addTenor(date(2024,6,15),"1w","f",False))



''' 

# Tests
import unittest

class TestCalendar(unittest.TestCase):
    
    def setUp(self):
        self.calendar = Calendar("za+US")
    
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
