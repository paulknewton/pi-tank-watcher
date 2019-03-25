# Shell script to build status message
# Currently unused - planned to be used for displaying current
# status of a Raspberry Pi on the LCD screen
#
# Can be run via cron
#
echo -e WATER:54%\\nTIME:`date +"%H:%M %d/%m/%y"`\\nHOST:`hostname`\\nIP:`ifconfig | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}'`\\n`iwconfig wlan0 | grep -o 'ESSID.*" ' | sed 's/"//g'` [`iwconfig wlan0 | grep -o 'level=.*  ' | sed 's/level=//g' | sed 's/ //g'`]
