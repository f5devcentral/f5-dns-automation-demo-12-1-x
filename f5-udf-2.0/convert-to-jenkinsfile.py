#!/usr/bin/python
# helper script to convert shell script into Jenkins file
line = ""
print """echo 'Starting DNS Automation Demo'
stage('clone git repo') {
   node {
     git url: 'https://github.com/f5devcentral/f5-dns-automation-demo-12-1-x.git'
   }
}
stage('run demo') {
  node {
      echo 'running demo...'
      sh 'pwd'
      dir ('lib') {
                    
"""

for l in open('udf.sh'):
    l = l.strip()
    if l.endswith('\\'):
        line = l[:-1]
        continue
    else:
        line += l
        if line:
            print "                    sh '" + line + "'"
        line = ""

print """      }
  }
}
"""
