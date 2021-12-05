#!/bin/bash

files=`ls results/*.pcap`
outfile=results/all.csv
rm -f ${outfile}

echo "repetition;foffset;snr;received"
echo "repetition;foffset;snr;received" > ${outfile}

for f in ${files}
do
	repetition=`python -c "print \"${f}\".split(\"_\")[1]"`
	foffset=`python -c "print \"${f}\".split(\"_\")[2]"`
	snr=`python -c "print \"${f}\".split(\"_\")[3]"`
	echo "file ${f}  repetition ${repetition}  foffset ${foffset}  snr ${snr}"
	rcvd=`tshark -r ${f} | wc -l | tr -d " "`
	echo "${repetition};${foffset};${snr};${rcvd}"
	echo "${repetition};${foffset};${snr};${rcvd}" >> ${outfile}
done
