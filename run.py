import os
import time
import subprocess
PERIOD = 30
RETRY = 5
GATEWAY_ADDR = '192.168.1.1'
LOG_PATH = 'auto-shutdown.log'

def check():
    retry_count = 0
    while retry_count < RETRY:
        ping_result = subprocess.run(['ping', '-c', '1', GATEWAY_ADDR], stdout=subprocess.PIPE)
        if ping_result.returncode == 0:
            print('ping success after {} failure'.format(retry_count))
            return True
        else:
            retry_count += 1
    print('PING FAILURE ENCOUNTERED FOR {} TIMES'.format(RETRY))
    return False

if __name__ == '__main__':
    while True:
        if not check():
            with open(LOG_PATH, 'a', encoding='utf-8') as log_f:
                log_f.write('gateway ping failed on {}, shutdown\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            os.system('poweroff')
        time.sleep(PERIOD)
