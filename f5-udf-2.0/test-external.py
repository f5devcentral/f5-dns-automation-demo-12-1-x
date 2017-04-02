import subprocess
import time
import sys
ssh_cmd = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null".split()
has_d = False
has_e = False
for x in range(10):
    p = subprocess.Popen(ssh_cmd+[sys.argv[1],"curl www.f5demo.com/simple.php"],stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
    output = p.stdout.read()
#    print output
    if 'US-EAST-1D' in output:
        has_d = True
    elif 'US-EAST-1E' in output:
        has_e = True
    if has_d and has_e:
        print 'Success.  round-robin LB for external clients'
        sys.exit(0)
    time.sleep(1)
print 'Failed to detect round-robin LB for external clients'
sys.exit(1)
