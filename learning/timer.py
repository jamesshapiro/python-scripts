from datetime import datetime

total_seconds = 0
outfile = '/mnt/c/Users/james/Desktop/000 SA Pro time.txt'
separator = '='*12
speedup_factor = 1.75

def get_todays_date():
    now = datetime.now()
    return f'{now.month:02d}-{now.day:02d}-{now.year}'

def get_display_time(seconds, prefix):
    mins = seconds // 60
    secs = seconds % 60
    spaces = ' ' * (6 - len(f'{prefix}:'))
    return f'{prefix}:{spaces}{mins}m{secs}'

lines = []
while(True):
    time_input = input('time: ')
    if time_input == '':
        break
    min_secs = time_input.split('m')
    seconds = int(min_secs[1].replace('s',''))
    minutes_in_seconds = int(min_secs[0])*60
    total_seconds += seconds
    total_seconds += minutes_in_seconds
    vid_seconds = 0
    vid_seconds += seconds
    vid_seconds += minutes_in_seconds
    vid_time = get_display_time(vid_seconds, 'time')
    lines.append(vid_time)
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
    f.write(get_todays_date() + '\n')
    f.write(separator + '\n')
    f.write('>\n')
    f.write('\n'.join(lines))

    
