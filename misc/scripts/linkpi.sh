set timeout -1
spawn ssh pi@ydchen.cn -oPort=12345
expect "*assword:*"
send "XXXXXXXXXXXXXXXXXXXXXXXX\r"
expect "*login*"
send "sudo su\r"
interact
