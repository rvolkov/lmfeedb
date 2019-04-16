# lmfeedb
feedback device


RJ45 on RPI
pin 8 from left on connector
GROUND
pin 7 - GROUND with resistor for LED

pin 1 - thumb


LED - short this is GROUND
on gloves Ground with resistor - RED
Ground - orange
White - line


# how to run it automatically on RPI
/etc/rc.local

cd /home/pi/lmfeedb
git pull
/usr/bin/python /home/pi/lmfeedb/run.py &

/etc/dhcpcd.conf
has part to configure fallback ip addr 192.168.0.253 with default gateway 192.168.0.1
(if DHCP is not available)

profile static_eth0
static ip_address=192.168.0.253/24
static routers=192.168.0.1
interface eth0
fallback static_eth0
