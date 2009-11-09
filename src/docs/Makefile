prefix = /usr
datadir = $(prefix)/share
mandir = $(datadir)/man

txttargets = $(shell echo *.1.txt)
mantargets = $(patsubst %.1.txt, %.1, $(txttargets))
asciidocver=$(patsubst asciidoc, , $(shell asciidoc --version)
minorasciidocver=$(shell echo $(asciidocver) | cut -d"." -f2)

all: $(mantargets)

install: ksxml2cfg.1
	install -Dp -m0644 ksxml2cfg.1 $(DESTDIR)$(mandir)/man1/ksxml2cfg.1
clean:
	rm -f *.html *.xml *.1

%.1.html: %.1.txt
	-asciidoc -d manpage $<

%.1:  %.1.xml
	xmlto man $<

%.html: %.txt
	asciidoc $<

%.1.xml: %.1.txt

ifeq ( $(minorasccdocver), 2)
	asciidoc -f kstools.conf -d manpage $<
else
	asciidoc -b docbook -a manmanual=kstools -a mansource=kstools -d manpage $<
endif
