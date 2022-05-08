from datetime import datetime

now = datetime.now()
todays_date = f'{now.month:02d}-{now.day:02d}-{now.year}'
print(todays_date)
