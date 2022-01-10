# Dayz-Nitrado-Server-Monitor

1) Add your Nitrado Access token and Game Server ID in Settings.ini.
2) Install to host with python 2.7
3) Set up a cron job to execute the program every 10 minutes (or whichever you fancy) e.g

```*/10 * * * * python /home/user/scripts/Nitrado-DayZ-Monitor/monitor.py >> /home/user/scripts/Nitrado-DayZ-Monitor/log.txt 2>&1```
