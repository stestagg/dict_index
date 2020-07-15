HERE=$(shell pwd)
PYROOT = ${HERE}/python
PYROOT_L = $(notdir ${PYROOT})


results/%.json: ${PYROOT_L}/bin/python3 .has-requirements
	env PYTHONPATH=. ${PYROOT}/bin/python3 benchmark/main.py > results/$*.json


report:
	cd report && python make_report.py ../results/ ../docs/


.has-requirements: ${PYROOT_L}/bin/python3 requirements.txt
	${PYROOT}/bin/pip3 install -r requirements.txt
	touch .has-requirements



${PYROOT_L}/bin/python3:  cpython/.ispatched
	- (cd cpython && make clean)
	(cd cpython && ./configure --cache-file=../config.cache --prefix=${PYROOT} --exec-prefix=${PYROOT})
	(cd cpython && make -j8 install)


cpython/.ispatched:
	(cd cpython && git apply ../changes.patch)
	touch cpython/.ispatched


.PHONY: report