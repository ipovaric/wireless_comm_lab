SHELL=/bin/bash

MESSAGES=100

PCAPFILES=$(shell python3 -c 'import itertools; import numpy as np; print(" ".join(["results/sim_%d_%.2f_%.1f_.pcap" % x for x in itertools.product(range(1), 0.03, np.arange(0, 15,.5))]))')

all: pdr.pdf

pdr.pdf: plot.py results/all.csv
	python3 ./plot.py

sim.py: sim.grc
	grcc sim.grc

results/all.csv: $(PCAPFILES)
	./parse.sh

%.pcap: sim.py
	@echo $@
	mkdir -p results
	export GR_CONF_DEFAULT_MAX_MESSAGES=123
	$(eval REPETITION=$(shell python -c "print \"$@\".split(\"_\")[1]"))
	$(eval FOFFSET=$(shell python -c "print \"$@\".split(\"_\")[2]"))
	$(eval SNR=$(shell python -c "print \"$@\".split(\"_\")[3]"))
	@echo REPETITION=$(REPETITION)
	@echo FOFFSET=$(FOFFSET)
	@echo SNR=$(SNR)
	./sim.py --messages=$(MESSAGES) --foffset=$(FOFFSET) --snr=$(SNR) --repetition=$(REPETITION)
#gdb -ex run -ex quit --args python ./sim.py --messages=$(MESSAGES) --foffset=$(FOFFSET) --snr=$(SNR) --repetition=$(REPETITION)

