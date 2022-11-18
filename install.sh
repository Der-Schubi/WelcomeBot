#!/bin/bash
systemctl stop welcomebot.service

mkdir -p /etc/welcomebot

cp ./welcomebot.py /etc/welcomebot/
cp ./.env /etc/welcomebot/
cp ./welcome_message.txt /etc/welcomebot/

chmod +x /etc/welcomebot/welcomebot.py
cp ./*.service /etc/systemd/system/
#cp ./*.timer /etc/systemd/system/

systemctl daemon-reload

systemctl start welcomebot.service
systemctl enable welcomebot.service
