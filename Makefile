.PHONY: build install dist sources clean

PROJECT := c2_ec2
PACKAGE := c2-ec2
PYTHON := python
VERSION := $(shell rpmspec -q --qf %{version} $(PACKAGE).spec)

build:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install --skip-build

dist: clean
	$(PYTHON) setup.py sdist

sources: clean
	@git archive --format=tar --prefix="$(PACKAGE)-$(VERSION)/" \
		$(shell git rev-parse --verify HEAD) | gzip > "$(PACKAGE)-$(VERSION).tar.gz"

clean:
	@rm -rf build $(PROJECT).egg-info $(PACKAGE)-*.tar.gz *.egg
