all:	unittest
unittest:	
	cd test && $(MAKE) test
clean:
	rm -f *~
	cd src && $(MAKE) clean
	cd test && $(MAKE) clean
