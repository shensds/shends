import ftp
f = ftp.FtpClicent()
f.host = "192.168.123.50"
f.port = 2121
f.login()
f.download("uc","e:\\uc")

