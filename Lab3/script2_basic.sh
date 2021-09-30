#!/bin/bash

hexdump sent_symbols.bin -v -e '1/1 "%02X\n"' > in.txt
hexdump recieved_symbols.bin -v -s 46 -e '1/1 "%02X\n"' > out.txt
sdiff in.txt out.txt > diff.txt
grep -o '<\|>\||' diff.txt | wc -l
