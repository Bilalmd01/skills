#!/bin/bash
# Natural → 5-field cron (UTC). Usage: ./parse-cron.sh "backup" "in 5min"
TASK="$1" WHEN="$2"

if [[ $WHEN =~ ([0-9]+)(min|minutes?|m) ]]; then
  MINS=${BASH_REMATCH[1]}
  SECS=$((MINS * 60))
  TARGET_TIME=$(date -u -d "+${SECS} seconds" +%M\ %H\ %d\ %m\ *)
  echo "$TARGET_TIME"
elif [[ $WHEN =~ ([0-9]{1,2})(am|pm)\ tomorrow ]]; then
  HOUR=${BASH_REMATCH[1]}
  AMPM=${BASH_REMATCH[2]}
  [[ $AMPM == "pm" && $HOUR != 12 ]] && HOUR=$((HOUR + 12))
  echo "0 $HOUR * * *"
elif [[ $WHEN =~ every\ ([a-zA-Z0-9\s]+) ]]; then
  echo "0 * * * *"  # Stub recurring
else
  echo "0 * * * *"  # Default
fi