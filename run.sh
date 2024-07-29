#!/bin/bash

if [ "$1" == "start" ]; then
    echo "Starting melo tts api server.."
    nohup python tts_api.py 1> /dev/null 2>&1 &
    sleep 1
elif [ "$1" == "stop" ]; then
    echo "Stopping melo tts api server.."
    sudo kill -9 `ps -ef|grep 'tts_api'|awk '{print $2}'`
    sleep 1
elif [ "$1" == "restart" ]; then
    echo "Restarting melo tts api server.."
    sudo kill -9 `ps -ef|grep 'tts_api'|awk '{print $2}'`
    sleep 3
    nohup python tts_api.py 1> /dev/null 2>&1 &
else
  echo "usage: ./start.sh start/stop/restart"
fi