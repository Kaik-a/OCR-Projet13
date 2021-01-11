#!/bin/bash
USER=$1
SAVE_DIRECTORY=$3

date=$(date +'%Y-%m-%d_%H:%M:%S')

pg_dump ocrprojet13 > "$SAVE_DIRECTORY"/full-"$date" -U "$USER"
