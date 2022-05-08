from datetime import datetime

total_seconds = 0
outfile = '/mnt/c/Users/james/Desktop/000 SA Pro time.txt'
separator = '='*12
speedup_factor = 1.75

def get_todays_date():
    now = datetime.now()
    return f'{now.month:02d}-{now.day:02d}-{now.year}'

def get_display_time(total_seconds, prefix):
    mins = total_seconds // 60
    secs = total_seconds % 60
    return f'{prefix}:  {mins}m{secs}'

lines = []
while(True):
    time_input = input('time: ')
    if time_input == '':
        break
    min_secs = time_input.split('m')
    total_seconds += int(min_secs[1].replace('s',''))
    total_seconds += int(min_secs[0])*60
    raw_time = get_display_time(total_seconds, 'raw')
    print(raw_time)
    lines.append(raw_time)
    at_higher_speed = int(total_seconds / speedup_factor)
    speedup_prefix = f'{speedup_factor:.2f}'.replace('.','')
    speed_time = get_display_time(at_higher_speed, speedup_prefix)
    print(speed_time)
    lines.append(speed_time)
    print(separator)
    lines.append(separator)
    if at_higher_speed >= 60*60:
        break

with open(outfile, 'w') as f:
    f.write(get_todays_date + '\n')
    f.write(separator + '\n')
    f.write('>\n')
    f.write('\n'.join(lines))

    
