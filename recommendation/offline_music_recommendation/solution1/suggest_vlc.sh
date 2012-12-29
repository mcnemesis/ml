#!/usr/bin/sh
./music_suggest.py $1 $2 | xargs vlc --play-and-exit
