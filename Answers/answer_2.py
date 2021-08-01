import formatter

def record_timeouts(log: str):
    log_time, server_address, response_time = log.split(',')
    response_time = response_time.replace('\n', '')

    try:
        response_time = int(response_time)
        if server_address in timeout_flags:
            if timeout_counts[server_address] >= N:
                formatter.format_log(server_address, timeout_flags[server_address], log_time, response_time)
            del timeout_flags[server_address]
            del timeout_counts[server_address]
    except ValueError:
        if server_address not in timeout_flags:
            timeout_flags[server_address] = log_time
            timeout_counts[server_address] = 1
        else:
            timeout_counts[server_address] += 1

def main():
    with open('LogData/sample2.txt') as file:
        for line in file:
            record_timeouts(line)
    for server_address, counts in timeout_counts.items():
        if counts >= N:
            formatter.format_still(server_address, timeout_flags[server_address])
    
if __name__ == '__main__':
    N = int(input('故障とみなすタイムアウトの回数：'))

    # {'server_address' : str サーバアドレス
    #  'start_time'     : str タイムアウト開始時間 この値があるならflagがTrueとする}
    timeout_flags = dict()

    # {'server_address':'timeout_counts'}
    timeout_counts = dict()

    main()