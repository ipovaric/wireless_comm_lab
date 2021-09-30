#!/bin/sh

# Author: Igor Povarich

# first clear files
rm in.txt
rm out.txt
rm diff.txt

# hexdump input file
hexdump sent_symbols.bin -v -e '1/1 "%02X\n"' > in.txt
# clip the last ## lines of in.txt
sed -i "$(( $(wc -l <in.txt)-55)),$ d" in.txt
# Note: skip first 46 lines from out.txt due to corrupted bytes
hexdump recieved_symbols.bin -v -s 46 -e '1/1 "%02X\n"' > out.txt
# difference bw two files
sdiff in.txt out.txt > diff.txt
# print BER
grep -o '<\|>\||' diff.txt | wc -l
wc -l diff.txt

# print truncated outputs
echo " Top of diff.txt:"
head -10 diff.txt
echo ""
echo "Bottom of diff.txt:"
tail -20 diff.txt
