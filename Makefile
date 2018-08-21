# Makefile for handling various tasks of Pylint sources
PYVE=pyve
PIP=$(PYVE)/bin/pip
TOX=$(PYVE)/bin/tox

VERSION=$(shell PYTHONPATH=. python -c "from pylint.__pkginfo__ import version; print(version)")

PKG_SDIST=dist/pylint-$(VERSION).tar.gz
PKG_DEB=../pylint_$(VERSION)-1_all.deb

# this is default target, it should always be first in this Makefile
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  tests       to run whole test suit of PyLint"
	@echo "  docs        to generate all docs including man pages and exemplary pylintrc"
	@echo "  deb         to build debian .deb package (it works only on Debian based Linux distros)"
	@echo "  sdist       to build source .tar.gz package"
	@echo "  lint        to check Pylint sources with itself"
	@echo "  all         to run all targets"


$(PIP):
	virtualenv $(PYVE)

$(TOX): $(PIP)
	$(PIP) install tox~=2.0


ifdef TOXENV
toxparams?=-e $(TOXENV)
endif

tests: $(TOX)
	$(TOX) $(toxparams)

docs: $(PIP)
	$(PIP) install .
	$(PIP) install Sphinx
	$(PIP) install python-docs-theme
	. $(PYVE)/bin/activate; make all -C doc

deb: $(PKG_DEB)
$(PKG_DEB): /usr/bin/debuild /usr/bin/dh_pysupport
	if [ -n "$$SUBVERSION" ]; then sed -i -e "0,/pylint (\(.*\))/s//pylint (\1.$${SUBVERSION})/" debian/changelog; fi
	debuild -b -us -uc

sdist: $(PKG_SDIST)
$(PKG_SDIST):
	python setup.py sdist

lint: $(PIP)
	$(PIP) install .
	$(PYVE)/bin/pylint lint.py || true  # for now ignore errors

clean:
	rm -rf $(PYVE)
	rm -rf .tox
	rm -rf dist
	rm -rf build
	make clean -C doc
	rm -rf $(PKG_DEB) ../pylint_*.changes ../pylint_*.build
	debuild clean || true


/usr/bin/debuild:
	sudo apt-get -y --force-yes install devscripts

/usr/bin/dh_pysupport:
	sudo apt-get -y --force-yes install python-support

all: clean lint tests docs sdist deb

.PHONY: help tests docs deb sdist lint clean all
