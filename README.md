### 通过IP查询Host name

下面是在Ubuntu服务器部署命令：

cd /var/

git clone https://github.com/sycct/Service_IP_Host.git

cd /var/Service_IP_Host

sudo apt-get install python-virtualenv -y

virtualenv venv -p /usr/bin/python3

. venv/bin/activate

pip install -r requirements.txt

sudo vi /etc/systemd/system/host_ip.service

cat > /etc/systemd/system/host_ip.service << EOF
```
[Unit]
Description=Get ip host name.
After=network.target
[Service]
User=root
Group=www-data
Environment="PATH=/var/Service_IP_Host/venv/bin/"
WorkingDirectory=/var/Service_IP_Host
ExecStart=/usr/bin/env python ip_host_main.py
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
[Install]
WantedBy=multi-user.target
```
EOF

systemctl start host_ip.service
