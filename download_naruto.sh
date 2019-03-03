#!/bin/bash

cd /home/rdepaiva/Documents/personal/python/anime

source anVenv/bin/activate

episodeList=$@
log="$HOME/Videos/Naruto/logs/$(date +%F)"
[ ! -d $log ] && mkdir -p $log

for epi in ${episodeList[@]}; do
    python anime.py $epi > $log/N$epi.log 2>&1 &
done

echo "Downloading episodes ${episodeList[@]}"
sleep 10
check_progress() {
    while true; do
        tput clear;
        for file in $log/N*; do
            echo "$file "
            grep kB $file;
        done;
        sleep 5
    done
}

check_progress
