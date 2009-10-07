all:	ksxml2cfg test
clean:
	rm -f ksxml2cfg
	rm -fr *~
	rm -fr *.pyc
	cd rhks && $(MAKE) clean
	cd data && rm -fr *~ && rm -fr *.cfg
test:
	@echo "testing ksxml2cfg.py"
	@for f in data/*.xml; \
	do \
		echo "compiling $$f" && \
		python ksxml2cfg.py "$$f";\
	done

ksxml2cfg:	ksxml2cfg.py
	@echo "creating shell script wrapper" && \
	echo "#!/usr/bin/python" >ksxml2cfg && \
	cat ksxml2cfg.py >>ksxml2cfg && chmod +x ksxml2cfg
