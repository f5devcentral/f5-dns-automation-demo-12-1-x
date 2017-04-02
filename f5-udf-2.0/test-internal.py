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
        print 'Failure.  round-robin LB for internal clients'
        sys.exit(1)
    time.sleep(1)
if has_d and sys.argv[2] == 'US-EAST-1E':
    print 'Failure.  Detected wrong Data Center'
    sys.exit(1)
elif has_e and sys.argv[2] == 'US-EAST-1D':
    print 'Failure.  Detected wrong Data Center'
    sys.exit(1)
elif not has_d and not has_e:
    print 'Failure.  Detected no Data Center'
    sys.exit(1)
print 'Success.  Affinity correct.'
