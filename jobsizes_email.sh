#!/bin/sh
JOBSDIR=$1
NEEDLE=$2
MAILFROM=$3
MAILTO=$4
MAILCC=$5
NOW=$(date +"%m/%d/%y")

/usr/local/bin/python2.7 /usr/local/python/jobfoldersizes/jobsizes.py --root="$JOBSDIR" --sort=size --filter="$NEEDLE" --output=email | mail -s "Job Sizes as of $NOW" -r "$MAILFROM" -c "$MAILCC" "$MAILTO"