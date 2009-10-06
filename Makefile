all:	unittest
unittest:	
	cd test && $(MAKE) test
	cd src && $(MAKE) test
clean:
	rm -f *~
	cd src && $(MAKE) clean
	cd test && $(MAKE) clean
