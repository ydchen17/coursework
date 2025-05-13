set timeout -1
spawn ssh pi@ydchen.cn -oPort=12345
expect "*assword:*"
send "145914\r"
expect "*login*"
send "sudo su\r"
interact
