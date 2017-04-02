echo 'Starting DNS Automation Demo'
stage('clone git repo') {
   node {
     git url: 'https://github.com/chen23/f5-dns-automation-demo-12-1-x.git'
   }
}
stage('run demo') {
  node {
      echo 'running demo...'
      sh 'pwd'
      dir 'f5-udf-2.0'
      sh 'pwd'
      sh 'sh udf.sh'
  }
}
