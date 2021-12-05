#!/bin/bash

files=`ls results/*.pcap`
outfile=results/all.csv
rm -f ${outfile}

echo "repetition;noise;snr;received"
echo "repetition;noise;snr;received" > ${outfile}

for f in ${files}
do
	repetition=`python -c "print \"${f}\".split(\"_\")[1]"`
	noise=`python -c "print \"${f}\".split(\"_\")[2]"`
	snr=`python -c "print \"${f}\".split(\"_\")[3]"`
	echo "file ${f}  repetition ${repetition}  noise ${noise}  snr ${snr}"
	rcvd=`tshark -r ${f} | wc -l | tr -d " "`
	echo "${repetition};${noise};${snr};${rcvd}"
	echo "${repetition};${noise};${snr};${rcvd}" >> ${outfile}
done
