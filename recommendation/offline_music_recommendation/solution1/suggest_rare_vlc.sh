#!/usr/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$DIR/music_suggest.py $1 $2 rare | xargs vlc --play-and-exit
