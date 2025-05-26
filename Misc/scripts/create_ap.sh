set timeout -1
spawn ssh pi@ydchen.cn -oPort=12345
expect "*assword:*"
send "XXXXXXXXXXXXXXXXXXX\r"
expect "login"
send "sudo su"
expect "/home/pi#"
send "nohup python3 zjunet.py > zjunet.log 2>&1 &"
nohup python3 zjunet.py > zjunet.log 2>&1 &$$nohup create_ap wlan0 eth0 FakeNet XXXXXXXXXXXXXXXXXXX > create_ap.log 2>&1 &"
