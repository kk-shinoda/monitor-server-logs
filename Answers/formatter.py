from datetime import datetime, timedelta

def format_datetime(YYYYMMDDhhmmss: str, delta=0) -> str:
    tmp = datetime.strptime(YYYYMMDDhhmmss, '%Y%m%d%H%M%S')
    tmp += timedelta(milliseconds=delta)
    if delta == 0:
        return tmp.strftime('%Y-%m-%d %H:%M:%S') 
    else:
        return tmp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def format_log(server_address: str, start_time: str, restore_time: str, response_time: int, error_name=''):
    start_time = format_datetime(start_time)
    end_time = format_datetime(restore_time) + str(response_time * (0.001))[1:]
    print('{0:<15}:{1:^25}~    {2:<25} {3}'.format(server_address, start_time, end_time, error_name))

def format_still(server_address, start_time, error_name=''):
    start_time = format_datetime(start_time)
    print('{0:<15}:{1:^25}~    {2:<25} {3}'.format(server_address, start_time, '', error_name))