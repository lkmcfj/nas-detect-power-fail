import os
import time
import subprocess
import sys
PERIOD = 30
RETRY = 5
GATEWAY_ADDR = '192.168.1.1'
LOG_PATH = 'auto-shutdown.log'

def log(msg):
    msg = '[{}]{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), msg)
    print(msg)
    with open(LOG_PATH, 'a', encoding='utf-8') as log_f:
        log_f.write(msg + '\n')

def check():
    retry_count = 0
    while retry_count < RETRY:
        ping_result = subprocess.run(['ping', '-c', '1', GATEWAY_ADDR], stdout=subprocess.PIPE)
        if ping_result.returncode == 0:
            log('ping success after {} failure'.format(retry_count))
            return True
        else:
            retry_count += 1
    log('PING FAILURE ENCOUNTERED FOR {} TIMES'.format(RETRY))
    return False

if __name__ == '__main__':
    while True:
        if not check():
            log('gateway ping failed, shutdown')
            os.system('poweroff')
            sys.exit()
        time.sleep(PERIOD)
