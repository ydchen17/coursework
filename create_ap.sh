set timeout -1
spawn ssh pi@ydchen.cn -oPort=12345
expect "*assword:*"
send "145914\r"
expect "login"
send "sudo su"
expect "/home/pi#"
send "nohup python3 zjunet.py > zjunet.log 2>&1 &"
nohup python3 zjunet.py > zjunet.log 2>&1 &$$nohup create_ap wlan0 eth0 FakeNet Cyd19980911 > create_ap.log 2>&1 &"
