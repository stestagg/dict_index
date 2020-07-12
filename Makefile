HERE=$(shell pwd)
PYROOT = ${HERE}/python
PYROOT_L = $(notdir ${PYROOT})


results/%.json: ${PYROOT_L}/bin/python3
	${PYROOT}/bin/python3 ${PYROOT}/bin/pip3 install -r requirements.txt
	env PYTHONPATH=. ${PYROOT}/bin/python3 benchmark/main.py > results/$*.json


${PYROOT_L}/bin/python3:  cpython/.ispatched
	- (cd cpython && make clean)
	(cd cpython && ./configure --cache-file=../config.cache --prefix=${PYROOT} --exec-prefix=${PYROOT})
	(cd cpython && make -j8 install)


cpython/.ispatched:
	(cd cpython && git apply ../changes.patch)
	touch cpython/.ispatched