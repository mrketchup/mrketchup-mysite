
def years_between(beginDate, endDate):
        try: # raised when birth date is February 29 and the current year is not a leap year
            begin = beginDate.replace(year=endDate.year)
        except ValueError:
            begin = beginDate.replace(year=endDate.year, day=beginDate.day-1)
        except AttributeError:
            return "?"
        if begin > endDate:
            return endDate.year - beginDate.year - 1
        else:
            return endDate.year - beginDate.year