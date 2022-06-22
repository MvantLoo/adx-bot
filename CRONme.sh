#!/bin/bash
cd ~/adx-bot

# Start the script if it had not generated any output for longer then 60 minutes
[[ $(date +%s -r adx_bot.log) -lt $(date +%s --date="60 min ago") ]] && python3 adx_bot.py

# CRON example to run every hour:
# 0 * * * * bash ~/adx-bot/CRONme.sh
