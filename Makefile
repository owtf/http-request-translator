default:
	@echo "'make check'" for tests

check:
	nosetests -v -d --with-cov
