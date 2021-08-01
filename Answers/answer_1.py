import formatter

def record_timeouts(log: str):
    log_time, server_address, response_time = log.split(',')
    response_time = response_time.replace('\n', '')

    try:
        response_time = int(response_time)
        if server_address in timeout_flags:
            formatter.format_log(server_address, timeout_flags[server_address], log_time, response_time)
            del timeout_flags[server_address]
    except ValueError:
        if server_address not in timeout_flags:
            timeout_flags[server_address] = log_time
        return

def main():
    with open('LogData/sample1.txt') as file:
        for line in file:
            record_timeouts(line)
    for server_address, start_time in timeout_flags.items():
        formatter.format_still(server_address, start_time)
    
if __name__ == '__main__':
    # {'server_address' : str サーバアドレス
    #  'start_time'     : str タイムアウト開始時間 この値があるならflagがTrueとする}
    timeout_flags = dict()
    main()