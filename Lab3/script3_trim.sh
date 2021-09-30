#!/bin/sh

# trim the in.txt file for file stopping variation
TRIM=12
sed -i "$(( $(wc -l <in.txt)-$TRIM+1)),$ d" in.txt
# re-run the hexdump and diff
sdiff in.txt out.txt > diff.txt
grep -o '<\|>\||' diff.txt | wc -l

tail -10 script3_trim.sh
