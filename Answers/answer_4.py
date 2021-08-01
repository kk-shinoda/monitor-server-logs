import formatter
import re

def rewrite_server_address(divided_address, prefix):
    filled_bin = ''
    for i in divided_address:
        filled_bin += (str(bin(int(i))[2:]).zfill(8))
    filled_bin = ''.join(list(reversed(filled_bin)))
    network_address_bin_reversed = filled_bin[32-prefix:]
    network_address_bin_reversed = network_address_bin_reversed.zfill(32)
    network_address_bin = ''.join(list(reversed(network_address_bin_reversed)))
    network_address = [str(int(network_address_bin[:8], 2)), str(int(network_address_bin[8:16], 2)),
                        str(int(network_address_bin[16:24], 2)), str(int(network_address_bin[24:], 2))]
    return '.'.join(network_address)

def record_timeouts(log: str):
    log_time, server_address, response_time = log.split(',')
    divided_address = re.split('\.|/', server_address)

    network_address_length = int(divided_address[-1])
    server_address = rewrite_server_address(divided_address[:-1], network_address_length)

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
    with open('LogData/sample1.txt') as file:
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

    # {'server_address'　   : str サーバアドレス
    # 　'timeout_counts'}   : int そのサーバがタイムアウトを返した回数
    timeout_counts = dict()
    main()