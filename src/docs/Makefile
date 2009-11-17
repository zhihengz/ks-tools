prefix = /usr
datadir = $(prefix)/share
mandir = $(datadir)/man

txttargets = $(shell echo *.1.txt)
mantargets = $(patsubst %.1.txt, %.1, $(txttargets))
asciidocver=$(patsubst asciidoc, , $(shell asciidoc --version 2>/dev/null))
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

ifeq ($(asciidocver),8.2.5)
	@echo "using own docbook conf since it is ascii $(asciidocver)"
	asciidoc -f kstools.conf -d manpage $<
else
	@echo "using default docbook since it is ascii $(asciidocver)"
	asciidoc -b docbook -a manmanual=kstools -a mansource=kstools -d manpage $<
endif
