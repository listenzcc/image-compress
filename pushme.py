import subprocess
import shlex
import time

for i in range(1000000000):
    print('Try {}'.format(i))
    command = 'git push -u origin main'
    ret = subprocess.call(shlex.split(command))
    print(ret)
    if ret == 0:
        break

    time.sleep(1)
