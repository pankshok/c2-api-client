.PHONY: build install dist sources srpm rpm clean

DIST := epel-6-x86_64
PROJECT := c2_ec2
PACKAGE := c2-ec2
PYTHON := python
VERSION := $(shell rpmspec -q --qf %{version} $(PACKAGE).spec)
RELEASE := $(shell rpmspec -q --qf %{release} $(PACKAGE).spec)

build:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install --skip-build

dist: clean
	$(PYTHON) setup.py sdist

sources: clean
	@git archive --format=tar --prefix="$(PACKAGE)-$(VERSION)/" \
		$(shell git rev-parse --verify HEAD) | gzip > "$(PACKAGE)-$(VERSION).tar.gz"

srpm: sources
	rpmbuild -bs --define "_sourcedir $(CURDIR)" \
		--define "_srcrpmdir $(CURDIR)" $(PACKAGE).spec

rpm:
	@mkdir -p rpm/$(DIST)
	/usr/bin/mock -r $(DIST) \
		--rebuild $(PACKAGE)-$(VERSION)-$(RELEASE).src.rpm \
		--resultdir rpm/$(DIST)

clean:
	@rm -rf build dist $(PROJECT).egg-info $(PACKAGE)-*.tar.gz *.egg *.src.rpm
