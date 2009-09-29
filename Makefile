all:	unittest
unittest:	
	cd test && $(MAKE) test
clean:
	rm -f *~
	cd src/rhks && $(MAKE) clean
	cd test && $(MAKE) clean
