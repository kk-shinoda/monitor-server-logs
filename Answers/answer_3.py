import formatter

def record_overloads(log: str):
    log_time, server_address, response_time = log.split(',')
    response_time = response_time.replace('\n', '')
    try:
        response_time = int(response_time)
    except ValueError:
        if server_address in overload_flags:
            formatter.format_log(server_address, overload_flags[server_address], log_time, 0, '過負荷(TO前)')
            del overload_flags[server_address]
        return

    if server_address not in recent_logs_by_sa:
        recent_logs_by_sa[server_address] = [{'start_time': log_time, 'response_time': response_time}]
        recent_response_time[server_address] = response_time
    else:
        recent_logs_by_sa[server_address].append({'start_time': log_time, 'response_time': response_time})
        recent_response_time[server_address] += response_time
        if len(recent_logs_by_sa[server_address]) > m: 
            recent_response_time[server_address] -= recent_logs_by_sa[server_address][0]['response_time']
            del recent_logs_by_sa[server_address][0]

    if recent_response_time[server_address]/len(recent_logs_by_sa[server_address]) > t:
        if server_address not in overload_flags:
            overload_flags[server_address] = log_time
    elif server_address in overload_flags:
        formatter.format_log(server_address, overload_flags[server_address], log_time, response_time, '過負荷状態')
        del overload_flags[server_address]

def record_timeouts(log: str):
    log_time, server_address, response_time = log.split(',')
    response_time = response_time.replace('\n', '')

    try:
        response_time = int(response_time)
        if server_address in timeout_flags:
            if timeout_counts[server_address] >= N:
                formatter.format_log(server_address, timeout_flags[server_address], log_time, response_time,'タイムアウト')
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
            record_overloads(line)
            
    for server_address, counts in timeout_counts.items():
        if counts >= N:
            formatter.format_still(server_address, timeout_flags[server_address], 'タイムアウト')
    for server_address, start_time in overload_flags.items():
        formatter.format_still(server_address, start_time, '過負荷状態')

if __name__ == '__main__':
    N = int(input('故障とみなすタイムアウトの回数：'))
    m = int(input('考慮する直近の応答時間の数：'))
    t = int(input('過負荷とするしきい値：'))
    
    # {'server_address' : str サーバアドレス
    #  'start_time'     : str タイムアウト開始時間 この値があるならflagがTrueとする}
    timeout_flags = dict()

    # {'server_address'　   : str サーバアドレス
    # 　'timeout_counts'}   : int そのサーバがタイムアウトを返した回数
    timeout_counts = dict()

    # {'server_address' : str サーバアドレス
    #  'start_time'     : str タイムアウト開始時間 この値があるならflagがTrueとする}
    overload_flags = dict()

    # サーバアドレスごとの前m回の応答時間の合計　平均応答時間を算出のに使用する
    # {'serve_address' :       :  str サーバアドレス
    #  'recent_response_time   :  int 前m回の応答時間の合計'}
    recent_response_time = dict()

    # 前m回のサーバアドレスごとのログ
    # {'server_address',    : str サーバアドレス 
    # [{'start_time',        : str 確認時間
    #  'response_time'}]}    : int 応答時間(ms)
    recent_logs_by_sa = dict()
    main()