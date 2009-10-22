TARGET=rpm
DIST=fc11
all:	unittest
unittest:	
	cd test && $(MAKE) test
	cd src && $(MAKE) test
clean:
	rm -f *~ ks-tools.spec.in
	cd src && $(MAKE) clean
	cd test && $(MAKE) clean
	rm -fr build

rpm:	ks-tools.spec.in
	rpmpkgbuild $(TARGET)

ks-tools.spec.in:	ks-tools.spec.in.template
	cat ks-tools.spec.in.template | \
	sed -e "s#DIST#.$(DIST)#g" > ks-tools.spec.in
