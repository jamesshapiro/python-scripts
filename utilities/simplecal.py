import calendar
import datetime
import sys

if __name__ == '__main__':
    now = datetime.datetime.now()
    cal = calendar.TextCalendar(firstweekday=6)
    if len(sys.argv) == 2:
        num_months = int(sys.argv[1])
    else:
        num_months = 3
    months = []
    curr_month = now.month
    curr_year = now.year
    for _ in range(num_months):
        text_month = cal.formatmonth(curr_year, curr_month)
        month_lines = text_month.split('\n')
        month_lines = [line + ' ' * (21 - len(line)) for line in month_lines]
        months.append(month_lines)
        curr_year = curr_year if curr_month < 12 else curr_year + 1
        curr_month = curr_month + 1 if curr_month < 12 else 1
    zipped = zip(*(month for month in months))
    for line in zipped:
        print(' '.join(line))
        
