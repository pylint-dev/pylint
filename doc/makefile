MKHTML=mkdoc
MKHTML_OPT=--doctype article --param toc.section.depth=1  --target html --stylesheet single-file

SRC=.


all: quickstart.html features.html FAQ.html examples man

FAQ.html: ${SRC}/FAQ.txt
	${MKHTML} ${MKHTML_OPT} ${SRC}/FAQ.txt

quickstart.html: ${SRC}/quickstart.txt
	${MKHTML} ${MKHTML_OPT} ${SRC}/quickstart.txt

features.html:
	chmod u+w ${SRC}/features.txt
	echo "PyLint features" > ${SRC}/features.txt
	echo "===============" >> ${SRC}/features.txt
	echo "" >> ${SRC}/features.txt
	echo ".. contents::" >> ${SRC}/features.txt
	echo "" >> ${SRC}/features.txt
	pylint --list-msgs >> ${SRC}/features.txt
	${MKHTML} ${MKHTML_OPT} ${SRC}/features.txt

examples:
	chmod u+w ../examples/pylintrc
	pylint --generate-rcfile > ../examples/pylintrc

man:
	chmod u+w ../man/pylint.1
	pylint --generate-man > ../man/pylint.1

clean:
	rm -f *.html

.PHONY: features.html
