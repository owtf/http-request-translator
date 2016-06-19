default:
	@echo "'make install[2]' for installation"
	@echo "'make check[2]' for tests"

install:
	python ./setup.py install

install2:
	python2 ./setup.py install

check:
	nosetests -v -d --with-cov

check2:
	nosetests2 -v -d --with-cov
