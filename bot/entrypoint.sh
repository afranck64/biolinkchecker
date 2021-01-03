#!/bin/bash

echo "Configure cron jobs"

LOG_FILE="/code/logs/cron.log"
WORKING_DIR="/code/bot/"
COMMAND_LOCK="/usr/bin/flock -n /code/bot/"
COMMAND_LOCK=
BASE_COMMAND="/usr/local/bin/python -m bot.main"
FULL_COMMAND="cd $WORKING_DIR && $COMMAND_LOCK $BASE_COMMAND"
echo " Fetch schedule: $CRON_SCHEDULE_FETCH $FULL_COMMAND"
echo " Check schedule: $CRON_SCHEDULE_CHECK"
echo "Notify schedule: $CRON_SCHEDULE_NOTIFY"
echo "cron logs: $LOG_FILE"

# Make sure not to clone the same tasks in the crontab
BASE_CRONTAB="/tmp/crontab"
echo "#Crontab" > $BASE_CRONTAB
crontab $BASE_CRONTAB

(crontab -l ; echo "$CRON_SCHEDULE_FETCH $FULL_COMMAND fetch 2>&1 >> $LOG_FILE ") | crontab
if [ "$CHECK_NOTIFY" ]
then
    echo "Separate check and notify"
    (crontab -l ; echo "$CRON_SCHEDULE_CHECK $FULL_COMMAND check 2>&1 >> $LOG_FILE ") | crontab
    (crontab -l ; echo "$CRON_SCHEDULE_NOTIFY $FULL_COMMAND notify 2>&1 >> $LOG_FILE") | crontab
else
    echo "check-notify in one step"
    (crontab -l ; echo "$CRON_SCHEDULE_CHECK_NOTIFY $FULL_COMMAND check-notify 2>&1 >> $LOG_FILE") | crontab
fi

echo "Configured cron jobs"

echo "Starting cron..."
cron -f -l -L 8
